# Memory Stress Application

A Python CLI application that gradually increases memory allocation until it causes an Out of Memory (OOM) error.

## Usage

### Running directly

```bash
python memory_stress.py <initial_memory> <final_memory> <duration> <initial_wait>
```

### Running with Docker

1. Build the Docker image:
```bash
docker build -t memory-stress .
```

2. Run the container:
```bash
docker run memory-stress <initial_memory> <final_memory> <duration> <initial_wait>
```

Example:
```bash
# Start with 100MB, wait 30 seconds, then reach 1GB in 60 seconds
docker run memory-stress 100 1024 60 30
```

### Arguments

- `initial_memory`: Initial memory allocation in MB
- `final_memory`: Final memory allocation in MB (will cause OOM)
- `duration`: Time in seconds for incremental allocation after initial wait
- `initial_wait`: Time in seconds to wait after initial allocation before starting incremental allocation

## Requirements

- Python 3.6 or higher (when running directly)
- Docker (when running in container)

## How it Works

1. The application first allocates the initial amount of memory specified
2. It then waits for the specified initial wait time
3. After the wait, it gradually increases memory allocation over the specified duration
4. Memory is allocated in 1KB chunks and filled with random data
5. The application will eventually trigger an OOM error when it reaches the system's memory limit

## Notes

- The application uses Python's `bytearray` to allocate memory
- Memory allocation is done in small increments to ensure smooth progression
- The application can be interrupted with Ctrl+C at any time
- When running in Docker, the container will be killed by Docker when it hits the OOM condition