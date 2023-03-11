FROM python:3.10

WORKDIR /

COPY . /
RUN pip install --no-cache-dir -r requirements.txt 

# 设置环境变量
ENV REFRESH_TOKEN=""
ENV RSS_URL=""
ENV BOT_TOKEN=""
ENV CHANNEL_ID=""
ENV RSS_SECOND=300
ENV PROXY="socks5://127.0.0.1:8089"
ENV PROXY_OPEN=False
ENV RSS_OPEN=True
ENV LOG_OPEN=True
ENV FILE_DELETE=True

CMD ["python", "main.py"]
