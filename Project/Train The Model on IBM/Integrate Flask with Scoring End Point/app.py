{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "451a69a5",
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'flask_cors'",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "\u001b[1;32m<ipython-input-1-d22871a15b9a>\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[0;32m      1\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mflask\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      2\u001b[0m \u001b[1;32mfrom\u001b[0m \u001b[0mflask\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mrequest\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mrender_template\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m----> 3\u001b[1;33m \u001b[1;32mfrom\u001b[0m \u001b[0mflask_cors\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mCORS\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m      4\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mjoblib\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      5\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mpandas\u001b[0m \u001b[1;32mas\u001b[0m \u001b[0mpd\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;31mModuleNotFoundError\u001b[0m: No module named 'flask_cors'"
     ]
    }
   ],
   "source": [
    "import flask\n",
    "from flask import request, render_template\n",
    "from flask_cors import CORS\n",
    "import joblib\n",
    "import pandas as pd\n",
    "from xgboost import XGBRegressor\n",
    "import requests\n",
    "app = flask.Flask(__name__)\n",
    "CORS(app)\n",
    "\n",
    "# purposely kept API KEY since cuh is very less\n",
    "\n",
    "API_KEY = \"t1xJwH_pNvesyStso2tawTlpypHX0HEQJVMev99cmAtK\"\n",
    "token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={\"apikey\":API_KEY, \"grant_type\": 'urn:ibm:params:oauth:grant-type:apikey'})\n",
    "mltoken = token_response.json()[\"access_token\"]\n",
    "\n",
    "header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}\n",
    "\n",
    "\n",
    "@app.route('/', methods=['GET'])\n",
    "def home():\n",
    "    return render_template('index.html')\n",
    "\n",
    "@app.route('/about')\n",
    "def about():\n",
    "    return render_template('about.html')\n",
    "\n",
    "@app.route('/predict')\n",
    "def predict():\n",
    "    return render_template('predict.html')\n",
    "\n",
    "@app.route('/services')\n",
    "def services():\n",
    "    return render_template('services.html')\n",
    "\n",
    "\n",
    "@app.route('/contact')\n",
    "def contact():\n",
    "    return render_template('contact.html')\n",
    "\n",
    "@app.route('/windapi',methods=['POST'])\n",
    "def windapi():\n",
    "    city=request.form.get('city')\n",
    "    apikey=\"86b1a085e43cad23bfd9c45d5fd88fc3\"\n",
    "    url=\"http://api.openweathermap.org/data/2.5/weather?q=\"+city+\"&appid=\"+apikey\n",
    "    resp = requests.get(url)\n",
    "    resp=resp.json()\n",
    "    temp = str(float(resp[\"main\"][\"temp\"])-273.15)+\" °C\"\n",
    "    humid = str(resp[\"main\"][\"humidity\"])+\" %\"\n",
    "    pressure = str(resp[\"main\"][\"pressure\"])+\" mmHG\"\n",
    "    speed = str(float(resp[\"wind\"][\"speed\"])*0.44704)+\" m/s\"\n",
    "    return render_template('predict.html', temp=temp, humid=humid, pressure=pressure, speed=speed)\n",
    "@app.route('/y_predict',methods=['POST'])\n",
    "def y_predict():\n",
    "    ws = float(request.form['theo'])\n",
    "    wd = float(request.form['wind'])\n",
    "    X = [[ws, wd]]\n",
    "    xgr = XGBRegressor()\n",
    "    df = pd.DataFrame(X, columns=['WindSpeed(m/s)', 'WindDirection'])\n",
    "    payload_scoring = {\"input_data\": [{\"field\": [['ws', 'wd']], \"values\":X}]}\n",
    "    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/0644c680-478f-475f-bc23-2a64fc6490a5/predictions?version=2022-10-24', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})\n",
    "    print(response_scoring)\n",
    "    predictions = response_scoring.json()\n",
    "    print(predictions)\n",
    "    output = predictions['predictions'][0]['values'][0][0]\n",
    "    print(\"Final prediction :\", predict)\n",
    "    return render_template('predict.html', prediction_text=\"The energy predicted is {:.2f} KWh\".format(output))\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3eab2c65",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
