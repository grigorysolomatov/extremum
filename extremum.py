import pandas as pd
import typer
import numpy as np
import json

app = typer.Typer()

help_string = '''
Returns indices of local minima and maxima of a csv column to standard output in json format:
{"min": [i1, i2, ..., in], "max": [j1, j2, ..., jn]}
'''

@app.command(help=help_string)
def main(data: str       = typer.Argument(help="Csv file"),
         column: str     = typer.Option(None, help="Column to consider, given by name"),
         radius: int     = typer.Option(5, help="Radius"),
         use_edges: bool = typer.Option(False, help="Include edges as potential minima or maxima")):

    df   = pd.read_csv(data)
    column  = column if column is not None  else df.columns[0]
    
    data   = df[column].values
    n      = len(data)
    padded = np.pad(data, pad_width=radius, mode="edge")

    maxs = [i - radius for i in range(radius, radius+n) if padded[i] == padded[i-radius:i+radius].max()]
    mins = [i - radius for i in range(radius, radius+n) if padded[i] == padded[i-radius:i+radius].min()]

    if not use_edges:        
        if maxs[0] == 0: maxs.pop(0)
        if maxs[-1] == n-1: maxs.pop(-1)
        if mins[0] == 0: mins.pop(0)
        if mins[-1] == n-1: mins.pop(-1)

    out = json.dumps({"min": mins, "max": maxs})
    print(out)
    
if __name__ == "__main__": app()


