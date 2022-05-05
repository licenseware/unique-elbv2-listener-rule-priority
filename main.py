#!/usr/local/bin/python

import argparse
import sys
import time
import logging
from random import randint, seed
from pprint import pformat

import boto3

parser = argparse.ArgumentParser()

parser.add_argument("--min-priority", type=int, default=1)
parser.add_argument("--max-priority", type=int, default=50_000)
parser.add_argument("--max-try", type=int, default=10_000)
parser.add_argument(
    "--log-level",
    type=str,
    choices=["debug", "info", "warning", "error"],
    default="error",
)

parser.add_argument("--listener-arn", type=str, required=True)
parser.add_argument("count", type=int)


def get_priorities(rules, exclude_priority: str | list[str] = "default") -> list[int]:
    if not isinstance(exclude_priority, list):
        exclude_priority = [exclude_priority]
    priorities = [
        rule["Priority"] for rule in rules if rule["Priority"] not in exclude_priority
    ]
    return list(map(int, priorities))


def get_random_priority(
    current_priorities: list[int],
    min_priority: int,
    max_priority: int,
    max_try: int,
    count: int = 1,
) -> int:
    for _ in range(count):
        for _ in range(max_try):
            priority = randint(min_priority, max_priority)
            if priority not in current_priorities:
                break
        else:
            raise Exception(f"Can't find a random priority in {current_priorities}")
        yield priority


def output_result(priorities: list[int]):
    value = ",".join(map(str, priorities))
    print(f"::set-output name=priorities::{value}", file=sys.stdout, flush=True)


if __name__ == "__main__":
    args = parser.parse_args(sys.argv[1:])

    seed(time.time())
    logging.basicConfig(level=args.log_level.upper())

    client = boto3.client("elbv2")
    response = client.describe_rules(ListenerArn=args.listener_arn)

    current_priorities = get_priorities(response["Rules"])

    logging.debug("Current priorities:")
    logging.debug(pformat(current_priorities))

    new_priorities = list(
        get_random_priority(
            current_priorities,
            args.min_priority,
            args.max_priority,
            args.max_try,
            args.count,
        )
    )

    logging.debug("New priorities:")
    logging.debug(pformat(new_priorities))

    output_result(new_priorities)
