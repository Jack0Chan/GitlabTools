# GitlabTools
Help to create new accounts, new groups and invite members to groups. Implemented with playwright.

# Environment

`pip install playwright`

- [playwright 入门教程](https://www.yuque.com/docs/share/4f709c9d-b649-4450-b791-4827c1e41e02?#)

If you have new requirements, please let me know :)

# Usage

```python
from GitLabTools import GitLabTools

students_info = pd.read_csv('students_profile.csv')
students_info = students_info.values
"""print(students_info)
# 这里的数据是从blackboard上下载下来的，分别是
    学号   姓名     学院      邮箱         身份
[[666666 '王王王' 'xx学院' 'wang@xxx.xx' '学生']
[777777 '李李李' 'xx学院' 'li@xx.xx' '学生']]
"""

gitlab = GitLabTools(gitlab_url='http://xxxxx/')
gitlab.sign_in(account='xxx', password='xxx')

# create new accounts
for student_info in students_info:
    mail = student_info[3]
    username = mail[:mail.index('@')]
    gitlab.create_new_account(name=username, username=username, mail=mail)

# create new groups
for i in range(11):
    team_name = f'team{i+1}'
    # print(team_name)
    gitlab.create_new_group(team_name)

# invite students to group
gitlab.invite_group_members(group_name='test_group', members=['wang', 'li'])

# create new blank project and assign to group 'test_group'
gitlab.create_new_blank_project('test_proj', 'test_group')
```

