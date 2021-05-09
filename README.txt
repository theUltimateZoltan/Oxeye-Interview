Instructions:
1. use pip to install requirements (pip install -r requirements.txt)
2. run server.py (change address configuration if needed: defaulted to 127.0.0.1:8000)
3. to add a component use POST args {name:"componentName"}, returns componentId in response body json object.
3. to add a connection between two components, use POST args {source:id, destination:id}, set source null to make direct
internet connection to destination. returns result in response body json.
4. to check flow to component use GET args {component: id} and check response body json for
{internetFacing:boolean, flow:componentsIdList}