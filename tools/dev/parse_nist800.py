import json
import sys

#{'source': 'asvs_v4.0.1', 'id': 'asvs_v4.0.1:14.1.3', 'id_raw': '14.1.3', 'tier_raw': 'Item', 'tier': 1, 'seq': None, 'title': None, 'description': 'Verify that server configuration is hardened as per the recommendations of the application server and frameworks in use.'}
sources = ['cis_csc_v7.1', 'nist_800_171_v1', 'nist_800_53_v4', 'nist_csf_v1.1', 'owasp_10_v3', 'asvs_v4.0.1']

nist_800_53_v4_mapping = {
  "ac":"access control",
  "at":"awareness and training",
  "au":"audit and accountability",
  "ca":"security assessment and authorization",
  "cm":"Configuration Management",
  "cp":"Contingency Planning",
  "ia":"Identification and Authentication",
  "ir":"Incident Response",
  "ma":"Maintenance",
  "mp":"Media Protection",
  "pe":"Physical and Environmental Protection",
  "pl":"Planning",
  "pm":"Program Management",
  "ps":"Personnel Security",
  "ra":"Risk Assessment",
  "sa":"System and Services Acquisition",
  "sc":"System and Communications Protection",
  "si":"System and Information Integrity",
}

nist_csf_mapping = {
  "de":"Detect",
  "de.ae":"Anomalies and Events",
  "de.cm":"Security Continuous Monitoring",
  "de.dp":"Detection Processes",
  "id":"Identify",
  "id.am":"Asset Management",
  "id.be":"Business Environment",
  "id.gv":"Governance",
  "id.ra":"Risk Assessment",
  "id.rm":"Risk Management Strategy",
  "id.sc":"Supply Chain Risk Management",
}
top=[]
control_map = {}
file = "controls.json"
with open(file) as f:
    controls=json.load(f)
    for index, control in enumerate(controls,1):
        if control.get("source") == "nist_800_53_v4":
          id = control.get("id_raw")
          category = nist_800_53_v4_mapping[id.split("-")[0].lower()]
          subcategory = control.get("tier_raw").lower() or category
          name = control["title"]
          description = control["description"]
          if name:
            name = name.replace("\u00a0"," ")
          if description:
            description = description.replace("\u00a0"," ")
          new_id = id
          if "(" in id:
              sub_number = id.split("(")[1].replace(")","")
              main_number = id.split("(")[0].strip()
              new_id = f'{main_number}.{sub_number}'
          else:
              new_id = new_id.replace(".","")
#haaaa
          new_id = new_id.lower()
          if "-" in new_id:
            ends_in_alpha = new_id[-1]

            if not ends_in_alpha.isdigit():
              #have subcontrols ending in a,b,c,d
              record = {
                "ref_code":new_id,
                "name":name or description,
                "description":description or name,
                "meta":{}
              }
              control_map[new_id[:-1]]["subcontrols"].append(record)
            else:
              record = {
                "name": name or description,
                "description": description or name,
                "ref_code": new_id,
                "system_level": False,
                "category": category,
                "subcategory": subcategory,
                "dti": "easy",
                "dtc": "easy",
                "meta": {},
                "subcontrols":[]
              }
              control_map[new_id] = record

#print(json.dumps(control_map,indent=4))
data = []
for ref,control in control_map.items():
  data.append(control)
print(json.dumps(data,indent=4))

#            control_map[name] = {"id":id,"category":category,"subcategory":control.get("tier_raw").lower() or category,"subcontrols":[]}
