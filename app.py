import gradio as gr
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn

from chatbot.master_agent import master_main


class GradioInterface:
    def __init__(self):
        self.demo = gr.ChatInterface(master_main).queue()

    def launch(self):
        # 手动启动 FastAPI 应用并添加 CORS 支持
        app = FastAPI()

        # 添加 CORS middleware 到 FastAPI 应用
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:5173"],  # 允许来自 Vue 开发服务器的请求
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # 将 Gradio 应用集成到 FastAPI 中
        app = gr.mount_gradio_app(app, self.demo, path="/")

        # 启动应用，监听特定端口
        try:
            uvicorn.run(app, host="0.0.0.0", port=7862)
        except KeyboardInterrupt:
            print("正在关闭服务器...")
        finally:
            # 确保资源被正确释放
            if hasattr(app, 'shutdown'):
                app.shutdown()


def main():
    interface = GradioInterface()
    interface.launch()


if __name__ == "__main__":
    main()
