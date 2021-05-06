### Problem:

In finance, it's common for accounts to have so-called "velocity limits". In this task, you'll write a program that accepts or declines attempts to load funds into customers' accounts in real-time.

Each attempt to load funds will come as a single-line JSON payload, structured as follows:

```json
{ "id": "1234", "customer_id": "1234", "load_amount": "$123.45", "time": "2018-01-01T00:00:00Z" }
```

Each customer is subject to three limits:

- A maximum of $5,000 can be loaded per day
- A maximum of $20,000 can be loaded per week
- A maximum of 3 loads can be performed per day, regardless of amount

As such, a user attempting to load $3,000 twice in one day would be declined on the second attempt, as would a user attempting to load $400 four times in a day.

For each load attempt, you should return a JSON response indicating whether the fund load was accepted based on the user's activity, with the structure:

```json
{ "id": "1234", "customer_id": "1234", "accepted": true }
```

You can assume that the input arrives in ascending chronological order and that if a load ID is observed more than once for a particular user, all but the first instance can be ignored. Each day is considered to end at midnight UTC, and weeks start on Monday (i.e. one second after 23:59:59 on Sunday).

Your program should process lines from `input.txt` and return output in the format specified above, either to standard output or a file. Expected output given our input data can be found in `output.txt`.

You're welcome to write your program in a general-purpose language of your choosing.

We value well-structured, self-documenting code with sensible test coverage. Descriptive function and variable names are appreciated, as is isolating your business logic from the rest of your code.


### Solution:

To process the payload attempts within the `input.txt` file, run the following code in your terminal:

```bash
python process_load_requests.py --input_path 'input.txt' --output_path 'python_output.txt'
```

The code above will output a `python_output.txt` file in the current directory; the responses in this file matches with those from `output.txt`.

Requirements: `python >= 3.6.3`.

### Code Design:

The business logic is stored in the `/takehome/velocity_limit/velocity_helpers.py` file.

`/takehome/velocity_limit/velocity_compile.py` contains the `velocity_limit_complier` class used to store and update customer information as the load attempts are passed in.

The assumption is that any duplicate load IDs, regardless if the first instance was accepted or rejected, will be ignored.
