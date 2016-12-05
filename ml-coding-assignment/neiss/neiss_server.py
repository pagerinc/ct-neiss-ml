from flask import Flask, request
from scorer.scorer import Scorer
from etl_utils.etl_constants import ColNames as cols
import numpy as np
app = Flask(__name__)

req_cols = list(cols.CRITICAL_COLS)
### TODO: make much more robust & refactor more modularly
@app.route('/api', methods=['GET'])
def hello_world():
    s = Scorer()
    try:
        arg_dict = dict(request.args)
        # impute any missing arguments w/ NaNs
        for col in req_cols:
            if col not in arg_dict:
                arg_dict[col] = np.nan
        result = s.score(arg_dict)
    except ValueError as e:
        return e.message
    if len(result) == 1:
        result = result[0]
    return '{0}'.format(result)