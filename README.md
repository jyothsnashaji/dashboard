# Dashboard for Router Health Monitor

A dashboard to add, view and monitor routers

## Getting Started


### Prerequisites

Python3

### Installing
use pip install to install the following
tensorflow,keras,pandas,numpy,dash,dash_bootstrap_components,pexpect

!!!make sure in the dash.py file "raise DuplicateOutputExceptions" is commented(line 975ish)!!!

## Running the tests

python3 index.py

to view the page click on the link generated. (localhost:://<port_number>)

python3 data_collect_10.py 

to connect to the router, start data collection and predictions

### Filewise explaination
1. assets folder : Contains all the images,stylesheets and javascript. For css and js to be included into the dashboard, checkout https://dash.plot.ly/external-resources

2.app.py : initialises an app object

3.index.py : conatins the main dash layout

4. callback.py : onevent functions. To change which file to be called when router added, change here

5. layouts.py : layouts of all pages

6.db.py: mongodb accesses

7. data_collect_10: connects to a hardcoded router and fetched health summary and predicts the parameters for the next 10 minutes.(Timestamps need fixing.lagging behind)

8. data_collect: predicts the parameters every one minute

9. db_csv.py: for testing with csv

10. Router_data.csv : random values to test the code

11. data_collection(2).py: one minute ahead prediction of cpu utilization


