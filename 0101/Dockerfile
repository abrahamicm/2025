FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

RUN pip install transformers
COPY . /app
WORKDIR /app
CMD ["python", "your_script.py"]
