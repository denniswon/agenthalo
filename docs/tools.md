# Contributing Tools to NewtonSwarm

## Overview

This guide will walk you through creating and contributing new tools to the NewtonSwarm ecosystem.
For general contributing guidelines, see [CONTRIBUTING.md](../CONTRIBUTING.md).

## Tool Architecture

Tools in NewtonSwarm follow a class-based architecture inheriting from `NewtonSwarmToolBase`. Each tool is designed to be:

- 🎯 **Single-Purpose**: Focused on one specific functionality
- 📝 **Self-Documenting**: Using Python docstrings and type hints
- 🔌 **Modular**: Easy to compose with other tools
- 🧪 **Testable**: With clear input/output contracts

## Creating a New Tool

### 1. Basic Structure

Create a new Python file in the appropriate subdirectory under `newtonswarm/tools/`. Here's a template for a new tool:

```python
from typing import Optional
from pydantic import BaseModel, Field

from newtonswarm.core.tool import NewtonSwarmToolBase

# Optional: Define input/output models if needed
# If you inherit from pydantic.BaseModel, schema information 
# will be automatically added to the tool's documentation and passed to the agent!
class MyToolOutput(BaseModel):
    result: str = Field(description="The result of the tool")
    confidence: float = Field(description="The confidence in the result, from 0 to 1")

class DoSomethingCool(NewtonSwarmToolBase):
    """
    A clear description of what your tool does.
    Include key features and any important notes about usage.
    That's what agent will see!
    """

    # Optional: Provide usage examples
    examples = [
       "Example 1", 
       "Example 2"
    ]

    def forward(self, input_value: str, optional_param: Optional[int] = None) -> MyToolOutput:
        """Process the input and return a result.

        Args:
            input_value: Description of the input value
            optional_param: Description of the optional parameter

        Returns:
            MyToolOutput object containing the result and confidence
        """
        # Implementation here
        return MyToolOutput(result="processed", confidence=0.95)
```

### 2. Key Components

#### Required Elements

1. **Class Documentation**:
   - Clear description of the tool's purpose
   - Usage notes and requirements
   - Any important caveats or limitations

2. **Type Hints**:
   - All parameters must have type hints
   - Return type must be explicitly defined
   - Use `Optional[]` for optional parameters

3. **Parameter Documentation**:
   - Each parameter must be documented in the `forward()` method's docstring
   - Follow the format: `param_name: Description of the parameter`

#### Optional Elements

1. **Usage Examples**:
   ```python
   examples = [
       "Here's when to use this tool:",
       "- When user asks to do something cool",
       "Here's how to use this tool"
       "- 'Do something cool with value 'abc'' -> DoSomethingCool(input_value='abc'). This will produce MyToolOutput(result='processed', confidence=0.95)"
   ]
   ```

2. **Input/Output Models**:
   - Use Pydantic models for structured data
   - Helps with validation and documentation

### 3. Best Practices

1. **Error Handling**:
   ```python
   def forward(self, input: str) -> Result:
       try:
           # Core logic here
           return Result(...)
       except ValueError as e:
           raise ValueError(f"Invalid input: {str(e)}") from e
       except Exception as e:
           raise RuntimeError(f"Unexpected error: {str(e)}") from e
   ```

2. **Input Validation**:
   - Validate inputs early
   - Provide clear error messages

3. **Documentation**:
   - Include docstrings for all public methods
   - Document any side effects
   - Provide usage examples

4. **Testing**:
   - Create unit tests in `tests/unit/tools/` - these are ones that are not dependent on external services
   - Create integration tests if needed in `tests/integration/tools/` - these are ones that could be dependent on external services, e.g. require API keys

## Integration Into the Repo

### 1. Directory Structure

Before creating a new tool category, ensure that none of the existing categories fits your new tool.

```
newtonswarm/
├── tools/
│   ├── tool_category/
│   │   ├── __init__.py
│   │   └── do_something_cool.py
│   └── __init__.py
└── tests/
    ├── unit/
    │   └── tools/
    │       └── tool_category/
    │           └── test_do_something_cool.py
    └── integration/
        └── tools/
            └── tool_category/
                └── test_do_something_cool.py
```

### 2. Naming Conventions

We use the following naming conventions for tools:

- Tool implementation files should be named without the `tool` suffix, as they are located in the `tools/` directory.
- Tool classes should be named without the `Tool` suffix.
- Tool classes names should reflect the action taken, e.g. `FetchTokenPrice` instead of `TokenPriceFetching`.

## Example Tools

For a complete example, refer to any tool in the `newtonswarm/tools/` directory.
Here are some examples:
- Tool that fetches the USD price of a token with CoinGecko API: [GetUsdPrice](../newtonswarm/tools/core/get_usd_price.py)
- Tool that uses Alchemy service: [GetAlchemyPriceHistoryBySymbol](../newtonswarm/tools/alchemy/alchemy_price_history.py)
- Tool that uses LLM to analyze trading strategies: [AnalyzeTradingStrategy](../newtonswarm/tools/strategy_analysis/generic/generic_analysis.py)

## Support

Need help? Check our [Discord](https://discord.gg/theoriq-dev) or open an issue on GitHub.

Remember: Tools are a critical part of NewtonSwarm's ecosystem. Well-designed tools make the entire system more powerful and useful for everyone.
