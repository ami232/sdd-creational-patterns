# Campaign Launchpad

You’re building a tiny backend service for a marketing team that launches online ad campaigns across multiple channels (e.g., Google Ads, Facebook Ads).

## Business requirements

- The company wants to keep track of the global budget when launching different campaigns.
- Marketers choose a channel and the system must create the right client to talk to that channel.
- Campaigns have many optional pieces (budget caps, audiences, creatives, tracking parameters). We need a safe way to assemble a valid campaign.

## Architecture

- **Builder**: `CampaignBuilder` assembles validated `Campaign` objects with a fluent API.
- **Singleton**: `GlobalBudget`, one shared marketing wallet for all campaigns.
- **Factory Method**: `ChannelClientFactory` creates channel-specific clients (Google, Facebook).

## Project layout

```dir_tree
root_dir
├─ campaign_launchpad/
│  ├─ __init__.py
│  ├─ budget.py
│  ├─ campaign.py
│  └─ channels.py
├─ tests/
│  ├─ test_budget.py
│  ├─ test_campaign.py
│  └─ test_channels.py
└─ README.md
```

## Setup

Preferred: [uv](https://docs.astral.sh/uv/). Install uv once per machine (see
uv's docs), then from inside your local clone:

```bash
uv venv                              # create a local virtual environment (.venv)
uv pip install -r requirements.txt   # install pytest into it
```

From then on, run any Python command through `uv run` so it uses that
environment automatically:

```bash
uv run pytest -q                            # run all tests
uv run pytest ./tests/test_budget.py        # run budget tests only
uv run python -m campaign_launchpad.app     # run the demo app
```

<details>
<summary>Alternative: plain venv + pip</summary>

```bash
# Unix
python -m venv .venv && source .venv/bin/activate

# Windows:
python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

python -m pytest -q
python -m pytest ./tests/test_budget.py
python -m campaign_launchpad.app
```

</details>

## How to submit

Two different repos are involved, so be precise about which is which:

- **The course repo** is `ami232/sdd-creational-patterns`.
  This is where your work has to end up. You cannot push to it, which is
  exactly why you send a pull request.
- **Your fork** is `<your-github-username>/sdd-creational-patterns`.
  This is where you do the work.

Every step below says which of the two it means. Where these instructions say
"the course repo", they never mean your fork, even though your fork contains
a copy of this same README.

1. Fork `ami232/sdd-creational-patterns` to your own GitHub account.
   Keep the fork **public** (the default when forking a public repo) so it can
   be reviewed without needing collaborator access.
2. Clone **your fork**, not the course repo, and work through the exercises
   below on a branch:

   ```bash
   git clone <the URL from the green "Code" button on your fork>
   cd sdd-creational-patterns
   git switch -c solution
   ```

3. Commit your changes and push the branch to your fork:

   ```bash
   git push origin solution
   ```

4. Open a **pull request from your fork into the course repo**. On github.com,
   open your fork, click "Contribute", then "Open pull request".

   Before you submit it, check that the pull request header reads exactly:

   | Field | Value |
   | --- | --- |
   | base repository | `ami232/sdd-creational-patterns` |
   | base | `main` |
   | head repository | `<your-github-username>/sdd-creational-patterns` |
   | compare | `solution` |

   **If your own username appears on both sides, the pull request is aimed at
   your own fork and will never reach us.** Change it with the "base
   repository" dropdown before submitting.
5. Opening the PR automatically runs the full test suite as a GitHub Actions
   check, see the "Checks" tab on your PR. All three test files
   (`test_budget.py`, `test_campaign.py`, `test_channels.py`) must pass for
   the check to go green.
6. Submit the link to your pull request on Blackboard. This is your
   submission; the green check confirms the tests pass, but the PR itself
   (with your commits and diff) is what gets graded.

## Exercises

### 1. Implement the campaign builder

`CampaignBuilder` assembles a `Campaign` through a fluent API: every `with_*`
and `add_*` method returns the builder itself so calls can be chained, and
`build()` is the only method that produces a `Campaign`.

Functional requirements:

- `build()` returns a `Campaign` that cannot be changed afterwards. Assigning
  to a field of a built campaign must raise.
- The end date is optional. A campaign with a start date and no end date is
  valid.
- `add_creative(headline, image_url)` may be called more than once, and at
  least one call is required.
- `with_audience(...)` and `with_tracking(...)` are optional and take keyword
  arguments.
- `build()` raises `ValueError` when something required is missing or
  inconsistent. The tests match on the message text, so each message must
  mention the field it is about:

  | Problem | The message must contain |
  | --- | --- |
  | No name | `name` |
  | No channel | `channel` |
  | Budget missing, zero or negative | `budget` |
  | No start date | `start date` |
  | Start date later than the end date | `start date` |
  | No creatives | `creative` |

  The match is case-insensitive, so `"Budget must be positive"` satisfies the
  `budget` row.

To test this part:

```bash
uv run pytest ./tests/test_campaign.py
```

Goal --> Pass campaign tests

### 2. Implement the global budget

`GlobalBudget` is a Singleton: there is exactly one marketing wallet, however
many times the class is constructed.

Functional requirements:

- `GlobalBudget(500.0)` and a later `GlobalBudget(9999.0)` must return the
  **same object**. The amount given on the first construction sets the
  balance, and amounts given to later constructions are ignored rather than
  overwriting it.
- `remaining()` returns the current balance.
- `allocate(amount)` subtracts `amount` from the balance.
- `allocate(amount)` raises `ValueError` when `amount` is zero or negative.
  Zero is rejected too, not only negative amounts.
- `allocate(amount)` raises `ValueError` when `amount` is greater than the
  remaining balance, and leaves the balance untouched. The balance can never
  go below zero.

To test this part:

```bash
uv run pytest ./tests/test_budget.py
```

Goal --> Pass budget tests

### 3. Implement the channel client factory

`ChannelClientFactory` is a Factory Method: callers name a channel and get
back a client for it without importing the concrete classes themselves.

Functional requirements:

- `ChannelClientFactory.create(channel)` returns a `GoogleAdsClient` for
  `"google"` and a `FacebookAdsClient` for `"facebook"`.
- `create(channel)` raises `ValueError` for any other channel name.
- Both clients implement the `ChannelClient` interface, so a caller can hold
  either one without knowing which.
- `client.create_campaign(campaign)` allocates the campaign's `daily_budget`
  **from** the shared `GlobalBudget`, then returns a new external id.
- That id starts with the first letter of the channel followed by a hyphen:
  `"g-<some_id>"` for Google Ads and `"f-<some_id>"` for Facebook Ads.
- Because the budget is shared, two clients built separately draw down the
  same balance.
- When a campaign's daily budget exceeds the remaining balance,
  `create_campaign` lets the `ValueError` from `allocate` propagate and
  returns no id.

To test this part:

```bash
uv run pytest ./tests/test_channels.py
```

Goal --> Pass channels tests
