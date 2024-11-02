import pandas as pd
import mysql.connector
from mysql.connector import Error
from llm.huggingface import llama_completion as llm_completion, message_builder


def ensure_sql_execute(system_message, message, sql, retry):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vcteva_2024",
            database="VCTEVA",
        )
        cursor = connection.cursor()
        cursor.execute(sql)
        column_names = [desc[0] for desc in cursor.description]
        result = cursor.fetchall()
        result_df = pd.DataFrame(result, columns=column_names)
        cursor.close()
        connection.close()

        # 可执行的SQL语句，输出刚刚执行的sql:
        print(sql)

        return result_df

    except Exception as e:
        retry += 1
        if retry <= 1:
            system_message_for_correction = "You are a SQL expert. Please fix the SQL query based on the error message and user request."

            error_msg = f"An error occurred: {e}"
            correction_message = f"Original SQL: {sql}\nError: {error_msg}\nPlease fix the SQL based on user request: {message}"

            sql = llm_completion(message_builder(
                system_message_for_correction, correction_message))
            print(error_msg)
            print(sql)

            return ensure_sql_execute(system_message, message, sql, retry)
        else:
            return False  # 重试超过1次就直接返回False


def sql_agent(message: str, history):
    system_message = '''You have to output SQL statements directly based on the statements you get, you can only output SQL statements without any comments.
        我们在下面提供了许多predefined sql，但是缺少parameters，你根据用户输入的query判断要执行哪个sql，并提供参数。
        重要的参数：year，league，tournament。

        如果你觉得predefined sql不能满足需求，你也可以自己写一个新的sql。
        
        你需要遵循以下规则：
        1. 只输出SQL语句，不要有任何注释
        2. 不允许使用CREATE和INSERT语句
        3. 如果使用predefined sql，需要替换其中的参数(例如《league》)
        4. 如果自己写SQL，需要确保语法正确且符合用户需求
        5. 尽量使用JOIN而不是子查询来提高性能
        6. 合理使用聚合函数和GROUP BY来处理数据
        7. 注意SQL注入的安全问题

        After the #### is an overview of the tables in the database you need to refer to.
        ###
        1. Players
        Column_Name:	Description
        player_id:	Primary key, unique identifier for each player (e.g., "109881619945257706").
        handle:	Player's in-game handle (e.g., "may").
        name:	Full name of the player (e.g., "Mayara Diniz").
        team_id:	Foreign key to reference the player's team.
        region:	Player's region (e.g., "LATAM").
        league:	League associated with the player (e.g., "game-changers").

        2. Tournaments
        Column_Name:	Description
        tournament_id:	Primary key, unique identifier for each tournament.
        player_id:	Foreign key, references the Players table.
        tournament_name:	Name of the tournament. Only one of items list below: ["game-changers-2022", "game-changers-2023", "game-changers-2024", "vct-challengers-2023", "vct-challengers-2024", "vct-international-2022", "vct-international-2023", "vct-international-2024"]

        3. Agents
        Column_Name:	Description
        agent_id:	Primary key, unique identifier for each agent (agent is the game character).
        map_id:	Foreign key, references the Maps table.
        games_win:	Number of games won by the agent in this map.
        games_count: 	Total number of games played by the agent in this map.

        4. Maps 
        Column_Name:	Description
        map_id:	Primary key, unique identifier for each map.
        tournament_id:	Foreign key, references the Tournaments table.
        map_name:	Name of the map (e.g., "Canyon").

        5. PerformanceDetails
        Column_Name:	Description
        performance_id:	Primary key, unique identifier for each performance record.
        agent_id:	Foreign key, references the Agents table.
        mode:	Mode of the game ("attacking" or "defending").
        kills:	Number of kills made by the player in this performance.
        deaths:	Number of deaths in the performance.
        assists:	Number of assists in the performance.
        rounds_taken:	Total number of rounds played.
        rounds_win:	Total number of rounds won by the player.
        cause:	JSON object storing details about the cause of certain events (e.g., {"SPIKE_DEFUSE": 9,"ELIMINATION": 32,"DETONATE": 2}).

        6. Summary
        Column_Name:	Description
        summary_id:	Primary key, unique identifier for summary.
        agent_id:	Foreign key, references the Agents table.
        combat_score:	Total combat score.
        average_combat_score:	Average combat score per round.
        kills:	Number of kills.
        deaths:	Number of deaths.
        assists:	Number of assists.
        kpr:	Kill-per-round ratio.
        dpr:	Death-per-round ratio.
        total_damage_taken:	Total damage taken by the player.
        total_damage_caused:	Total damage caused by the player.
        average_damage_per_round:	Average damage caused per round.
        average_damage_taken_per_round:	Average damage taken per round.
        ddelta:	Damage delta (difference between damage taken and caused).
        headshot_hit_rate:	Percentage of hits that were headshots.

        7. DamageDetails 
        Column_Name:	Description
        damage_id:	Primary key, unique identifier for each damage record.
        agent_id:	Foreign key, references the Agents table.
        type:	Type of damage (e.g., "Head", "Body", "LEG", "GENERAL").
        head_count:	Number of hits to the head.
        body_count:	Number of hits to the body.
        leg_count:	Number of hits to the legs.
        general_count:	General count of all hits.
        head_amount:	Total damage caused to the head.
        body_amount:	Total damage caused to the body.
        leg_amount:	Total damage caused to the legs.
        general_amount:	General amount of all damage caused.

        ###
        predefined sql：
            select * from Players where league = 《league》

            SELECT p.player_id, p.handle, p.name, AVG(pd.combat_score) AS average_combat_score
            FROM Players p
            JOIN Tournaments t ON p.player_id = t.player_id
            JOIN PerformanceDetails pd ON p.player_id = pd.agent_id
            WHERE t.tournament_name = 《para》
            GROUP BY p.player_id, p.handle, p.name
            ORDER BY average_combat_score DESC
            LIMIT 1;
    '''

    # 得到response中的sql语句之后，直接执行，然后将得到的数据返回。(json_to_str)
    sql = llm_completion(
        message_builder(system_message, message, history))

    if "create" in sql.lower() or "insert" in sql.lower():
        return False
    result_df = ensure_sql_execute(system_message, message, sql, 0)

    if isinstance(result_df, pd.DataFrame):  # 不管得到的数据是空与否
        df_json_string = result_df.to_json(orient='records', force_ascii=False)
        print(df_json_string)
        return df_json_string
    else:
        print("Check Database Status!")
        return False
