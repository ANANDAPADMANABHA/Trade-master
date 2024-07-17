# Trade Master: Algorithmic Trading Bot

Trade Master is an advanced algorithmic trading bot designed to automate the execution of various trading strategies in financial markets.
Integrated with SmartAPI, Trade Master accesses real-time market data from Angel One broker, allowing users to execute trades seamlessly.
With support for customizable trading strategies, real-time monitoring, risk management features, and platform compatibility,
Trade Master empowers traders to optimize their trading strategies, manage risks effectively, and capitalize on market opportunities with confidence

## Features

- **SmartAPI Integration**: Seamlessly integrates with SmartAPI to access real-time market data and execute trades on Angel One broker.
- **Multiple Trading Strategies**: Trade Master supports various trading strategies, including:
  - Opening Range Breakout Strategy
  - Yesterday High Breakout Strategy
  - Lot more in progress

## Getting Started

### Prerequisites

Before running Trade Master, ensure you have the following prerequisites installed:

- Python 3.6

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/ANANDAPADMANABHA/Trade-master.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Trade-Master
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Obtain API keys from Angel One broker.
2. Go to `config.py` and update the configuration settings with your API keys.

   ```python
   API_KEY = '{{API_KEY}}'
   CLIENT_ID = '{{CLIENT_ID}}'
   PASSWORD = '{{PASSWORD}}'
   TOKEN = '{{TOKEN}}'
   ```
### To run locally open 3 terminals
### Usage: Follow the steps and the bot will atumatically run everyday 9:20

Start Redis server:

```bash
redis-server
```

Run celery beat:

```bash
celery -A cronjobs beat --loglevel=info
```

Run worker:

```bash
celery -A cronjobs worker --loglevel=info
```

## Contributing

Contributions are welcome! If you'd like to contribute to Trade Master, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/new-feature`).
6. Create a new Pull Request.

## License

[Choose a license for your project and mention it here]

## Acknowledgements

We would like to thank the following individuals and organizations for their contributions, support, and inspiration:

- **Open-source Libraries**: We are grateful to the developers of [Library Name] for providing [description of how it helped].
- **API Providers**: We would like to acknowledge SmartAPI for providing the API used in this project.
- **Online Resources**: The tutorials and documentation from Angelone were instrumental in helping us understand api integration .

## Contact

For any inquiries or support, please contact ananthapadmanabhan012@gmail.com
