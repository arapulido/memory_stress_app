#!/usr/bin/env python3
import argparse
import time
import sys
from typing import List


def allocate_memory(mb: int) -> List[bytearray]:
    """
    Allocate memory in MB chunks and fill with a constant value.
    Each bytearray is 1KB in size and filled with the same byte value.
    """
    blocks = []
    kb = mb * 1024
    constant_value = 0x42
    for _ in range(kb):
        block = bytearray([constant_value] * 1024)
        blocks.append(block)
    return blocks


def main():
    parser = argparse.ArgumentParser(
        description='Memory stress application that gradually increases memory usage'
    )
    parser.add_argument(
        'initial_memory',
        type=int,
        help='Initial memory allocation in MB'
    )
    parser.add_argument(
        'final_memory',
        type=int,
        help='Final memory allocation in MB that will cause OOM'
    )
    parser.add_argument(
        'duration',
        type=int,
        help='Time in seconds to reach final memory after initial wait'
    )
    parser.add_argument(
        'initial_wait',
        type=int,
        help='Time in seconds to wait after initial allocation before starting incremental allocation'
    )

    args = parser.parse_args()

    if args.initial_memory >= args.final_memory:
        print("Error: Initial memory must be less than final memory")
        sys.exit(1)

    if args.duration <= 0:
        print("Error: Duration must be greater than 0")
        sys.exit(1)

    if args.initial_wait < 0:
        print("Error: Initial wait time cannot be negative")
        sys.exit(1)

    memory_increment = (args.final_memory - args.initial_memory) / args.duration
    current_memory = args.initial_memory

    print(f"Starting with {args.initial_memory}MB of memory")
    print(f"Will wait {args.initial_wait} seconds before starting incremental allocation")
    print(f"Will then reach {args.final_memory}MB in {args.duration} seconds")

    # Initial memory allocation
    memory_blocks = allocate_memory(args.initial_memory)
    print(f"Initial memory allocation complete: {args.initial_memory}MB")

    # Wait for initial wait time
    if args.initial_wait > 0:
        print(f"Waiting {args.initial_wait} seconds before starting incremental allocation...")
        time.sleep(args.initial_wait)
        print("Starting incremental allocation...")

    start_time = time.time()
    target_end_time = start_time + args.duration

    try:
        while current_memory < args.final_memory:
            current_time = time.time()
            if current_time >= target_end_time:
                # If we've reached the target time, allocate remaining memory
                remaining_memory = args.final_memory - current_memory
                if remaining_memory > 0:
                    new_blocks = allocate_memory(remaining_memory)
                    memory_blocks.extend(new_blocks)
                    current_memory = args.final_memory
                    print(f"Allocated final {remaining_memory}MB. Total: {current_memory}MB")
                break

            elapsed = current_time - start_time
            target_memory = args.initial_memory + (memory_increment * elapsed)

            # Only allocate if we need more memory
            if target_memory > current_memory:
                additional_memory = int(target_memory - current_memory)
                if additional_memory > 0:
                    new_blocks = allocate_memory(additional_memory)
                    memory_blocks.extend(new_blocks)
                    current_memory += additional_memory
                    print(
                        f"Allocated {additional_memory}MB more memory. "
                        f"Total: {current_memory}MB"
                    )

            # Calculate sleep time to maintain the target rate
            if current_memory < args.final_memory:
                next_target_time = start_time + (current_memory - args.initial_memory + 1) / memory_increment
                sleep_time = max(0.01, min(next_target_time - current_time, target_end_time - current_time))
                time.sleep(sleep_time)

        print(f"\nReached target memory of {args.final_memory}MB")

    except MemoryError:
        print(f"\nOOM Error occurred at {current_memory}MB allocation")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\nProcess interrupted. Final memory allocation: {current_memory}MB")
        sys.exit(0)


if __name__ == "__main__":
    main()