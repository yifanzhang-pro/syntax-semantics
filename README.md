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

To add colored boxes around each element in your GitHub README, you can use HTML `<div>` elements with inline CSS styles to specify the background color. Here's how you can do it for the "Training Corpus" section:

If you want the colored boxes around each element to be expanded by default when someone views your GitHub README, you can use a combination of HTML and JavaScript. Here's how you can achieve this:

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

<script>
document.getElementById("defaultOpen1").setAttribute("open", "true");
document.getElementById("defaultOpen2").setAttribute("open", "true");
document.getElementById("defaultOpen3").setAttribute("open", "true");
</script>
