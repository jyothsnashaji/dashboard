# Dashboard for Router Health Monitor

A dashboard to add, view and monitor routers
The dashoard computes and displays the health score for the router and classifies them as normal,warning or critical. There are four scores available, for router hardware health, software health, network health and the aggreagate summary. The scores are calculated from the router statistics polled every minute. When a new router is added a the polling for health stats starts. The data is stored into a mongo db and is used to train a LSTM model that will predict the future values.

## Getting Started


### Prerequisites

Python3

### Installations
use pip to install the following
- tensorflow
- keras
- pandas
- numpy
- dash
- dash_bootstrap_components,pexpect


## Running the tests

python3 index.py

 - To view the page click on the link generated. (localhost:://<port_number>)

python3 data_collect_10.py 

 - To connect to the router, start data collection and predictions

### Directory breakdown
1. assets : Contains all the images,stylesheets and javascript. For css and js to be included into the dashboard, refer https://dash.plot.ly/external-resources

2. app.py : Initialises an app object

3. index.py : contains the main dash layout

4. callback.py : onEvent functions. To specify which file to be called when router added, change here

5. layouts.py : Layouts of all pages

6. db.py: mongodb accesses

7. data_collect_10: connects to a hardcoded router and fetched health summary and predicts the parameters for the next 10 minutes.(Timestamps need fixing.lagging behind)

8. data_collect: predicts the parameters every one minute

9. db_csv.py: For testing with csv (import db_csv instead of db to test with Routerdata.csv instead of csv)

10. Router_data.csv : random values to test the code

11. data_collection(2).py: one minute ahead prediction of CPU utilization



