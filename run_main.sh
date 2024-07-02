kill -9 `ps -ef|grep "streamlit run CloudDemo.py"| awk 'NR==1 {print $2}'`
nohup streamlit run "CloudDemo.py" --server.port 8501 --server.enableXsrfProtection false &
ps -ef |grep streamlit
