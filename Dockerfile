FROM python:3.13-slim
WORKDIR /work
COPY pyproject.toml requirements-lock.txt ./
RUN pip install --no-cache-dir -r requirements-lock.txt
COPY . .
ENV OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
CMD ["python", "scripts/resume_remaining_search.py"]
