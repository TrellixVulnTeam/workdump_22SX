import subprocess
import re

run = lambda args: subprocess.check_output(args).decode('utf-8')
list_cmd = ["sh", "-c", "act -l | head -n 2 | tail -n 1"]
list_str = run(list_cmd)
workflows = re.findall("[a-z-]{2,}", list_str)
act_all_list = [f"act -j {workflow} -v" for workflow in workflows]
print(" && ".join(act_all_list))
print(" && ".join([a for a in act_all_list if "pydocstyle" not in a]))
# act_all_cmd = ["sh", "-c", " && ".join(act_all_list)]
# run_all_str = run(act_all_cmd)
# print(run_all_str)
