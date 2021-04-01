# coding=utf-8
# 启动程序
from apps import create_app

app = create_app()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=50006, debug=True)