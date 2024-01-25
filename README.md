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

**Training Corpus** should be looks like:

- Markdown version:

Q: {problem}

```python
{solution_code}
```
```output
{result}
```

{solution_wocode}


- XML version: 

```
"problem"

<code>
"solution_code"
</code>
<result>
"result"
</result>
"solution_wocode"
```
