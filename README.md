# TemplateMath

TemplateMath: Syntactic Data Generation for Mathematical Problems (https://huggingface.co/datasets/math-ai/TemplateGSM)

## Data Structure

```json
{
    "problem": "[problem]",
    "solution_code": "[commented code]",
    "solution_wocode": "[plain text solution]",
    "result": "[the numerical result]"
}
```

## Training Corpus

<div style="background-color: #f0f0f0; padding: 10px; border: 1px solid #dcdcdc;" id="defaultOpen1">
<details open>
<summary><b style="background-color: #007acc; color: #ffffff; padding: 5px;">solution() style:</b></summary>

```python
def solution():
    """
    {problem}
    """
    {solution_code}
    return result

print(result())
```
```output
{result}
```
{solution_wocode}

</details>
</div>

<div style="background-color: #f0f0f0; padding: 10px; border: 1px solid #dcdcdc;" id="defaultOpen2">
<details open>
<summary><b style="background-color: #007acc; color: #ffffff; padding: 5px;">Markdown version:</b></summary>

{problem}

```python
{solution_code}

print(result)
```
```output
{result}
```

{solution_wocode}

</details>
</div>

<div style="background-color: #f0f0f0; padding: 10px; border: 1px solid #dcdcdc;" id="defaultOpen3">
<details open>
<summary><b style="background-color: #007acc; color: #ffffff; padding: 5px;">XML version:</b></summary>

```xml
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

</details>
</div>
