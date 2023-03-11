FROM python:3.10

# 设置环境变量
# ENV PYTHONUNBUFFERED 1

# 设置工作目录
WORKDIR /

# 将项目依赖拷贝到容器中
COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt 

# 将项目代码拷贝到容器中
COPY . /

# 配置系统变量
ENV MY_VAR=value

# 运行项目
CMD ["python", "main.py"]
