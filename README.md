# Syntax-Semantics Learning

## Data Structure

```json
{
    "problem": "[problem]",
    "solution_code": "[commented code]",
    "solution_wocode": "[plain text solution]",
    "result": "[the numerical result]"
}
```

**Training Corpus** should be look like this:

- Markdown version:

Q: {problem}

A: Let's think step by step.
```python
{solution_code}
```
```output
{result}
```

{solution_wocode}


- XML version: 

```
<problem>
{problem}
</problem>
<code>
{solution_code}
</code>
<output>
{result}
</output>
<solution>
{solution_wocode}
</solution>
```
