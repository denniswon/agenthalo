
## Features

### Quote for a token pair

- Initializes the NewtonSwarm agent with a token price checking tool
- Uses Claude 3.5 Sonnet to process natural language queries
- Connects to Base network to fetch real-time token prices
- Demonstrates how to query token pair prices (AIXBT/USDC) using natural language

### Execute a token swap

- Initializes the NewtonSwarm agent with a token swap tool
- Uses Claude 3.5 Sonnet to process natural language queries
- Connects to Ethereum Sepolia network to execute a token swap
- Demonstrates how to initiate a token swap (3 USDC for WETH) using natural language

### Check trading strategy and optionally execute it

- Initializes the NewtonSwarm agent with both strategy analysis and token swap tools
- Uses Claude 3.5 Sonnet to process natural language queries
- Defines a simple trading strategy: Swap 3 USDC for WETH on Ethereum Sepolia when price below 10000 USDC per WETH
- Evaluates the trading strategy conditions using real-time market data when triggered
- Conditionally executes trades only when strategy conditions are met

### Make trading decisions based on price momentum signals and portfolio balances

- Implements a portfolio-aware momentum trading strategy using NewtonSwarm's agent framework
- Monitors multiple token prices on a schedule using Alchemy's price feed from a CronJobClient
- Evaluates both short-term (e.g. 5min) and long-term (e.g. 60min) price momentum signals to assess directional alignment (upward for buying or downward for selling)
- Makes a dynamic trading decision based on the above signals and the current token balances in the portfolio
- Additionally, the agent can be configured to limit individual trade sizes and maintain a minimum balance in your base token

## More Features

Check out the `interaction/` directory for more complete examples:
- [Command-line interface usage](interaction/terminal.py)
- [Setting up Telegram bot](interaction/telegram_bot.py)
- [Running strategies on a schedule](interaction/cron.py)
