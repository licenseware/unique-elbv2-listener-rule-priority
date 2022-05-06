#!/usr/bin/env python

import argparse
import sys
import time
import logging
from random import randint, seed
from pprint import pformat

import boto3

DEFAULT_DELIMITER = ","
DEFAULT_MIN_PRIORITY = 1
DEFAULT_MAX_PRIORITY = 50_000
DEFAULT_MAX_TRY = 10_000
DEFAULT_LOG_LEVEL = "error"


parser = argparse.ArgumentParser()

parser.add_argument("--min-priority", type=int, default=DEFAULT_MIN_PRIORITY)
parser.add_argument("--max-priority", type=int, default=DEFAULT_MAX_PRIORITY)
parser.add_argument("-r", "--max-try", type=int, default=DEFAULT_MAX_TRY)
parser.add_argument(
    "-l",
    "--log-level",
    type=str,
    choices=["debug", "info", "warning", "error"],
    default=DEFAULT_LOG_LEVEL,
)
parser.add_argument("-s", "--sorted", type=bool, default=False)
parser.add_argument("-d", "--delimiter", type=str, default=DEFAULT_DELIMITER)

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
    count: int,
    min_priority: int,
    max_priority: int,
    max_try: int,
) -> int:
    for _ in range(count):
        for _ in range(max_try):
            priority = randint(min_priority, max_priority)
            if priority not in current_priorities:
                break
        else:
            raise Exception(f"Can't find a random priority in {current_priorities}")
        yield priority


def output_result(priorities: list[int], delimiter: str):
    value = delimiter.join(map(str, priorities))
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

    listify = sorted if args.sorted else list

    new_priorities = listify(
        get_random_priority(
            current_priorities,
            min_priority=args.min_priority,
            max_priority=args.max_priority,
            max_try=args.max_try,
            count=args.count,
        )
    )

    logging.debug("New priorities:")
    logging.debug(pformat(new_priorities))

    output_result(new_priorities, delimiter=args.delimiter)
