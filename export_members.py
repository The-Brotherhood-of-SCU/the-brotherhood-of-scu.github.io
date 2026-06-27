import subprocess
import json
import sys

ORG_NAME = "The-Brotherhood-of-SCU"

def run_graphql(org_name):
    query = """
    query($org: String!) {
      organization(login: $org) {
        membersWithRole(first: 100) {
          edges {
            role
            node {
              login
              name
              bio
            }
          }
        }
      }
    }
    """
    
    cmd = [
        "gh", "api", "graphql",
        "-f", f"org={org_name}",
        "-f", f"query={query}"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return None
    return json.loads(result.stdout)

def main():
    print(f"# 正在获取 {ORG_NAME} 成员数据并排序...")
    
    data = run_graphql(ORG_NAME)
    
    if not data or 'data' not in data or not data['data']['organization']:
        print("未能获取数据。请确认组织名称正确且已执行 gh auth refresh -s read:org")
        return

    raw_members = data['data']['organization']['membersWithRole']['edges']
    
    processed_list = []
    for item in raw_members:
        node = item['node']
        role_type = item['role']
        
        processed_list.append({
            "login": node['login'].lower(),
            "original_login": node['login'],
            "name": node['name'] or node['login'],
            "role": role_type,
            "is_admin": role_type == "ADMIN",
            "bio": (node['bio'] or "没有介绍信息的高手...").replace('\r', '').replace('\n', ' ').replace(':', '：').strip()
        })

    sorted_members = sorted(processed_list, key=lambda x: (-x['is_admin'], x['login']))

    output_file = "./source/_data/members.yml"
    with open(output_file, "w", encoding="utf-8") as f:
        for m in sorted_members:
            f.write(f"- name: {m['name']}\n")
            f.write(f"  github: {m['original_login']}\n")
            f.write(f"  role: {m['role']}\n")
            f.write(f"  bio: {m['bio']}\n\n")
            print(f"[{m['role']}] {m['original_login']}")

    print(f"\n✅ 导出成功！共 {len(sorted_members)} 位成员，已保存至 {output_file}")

if __name__ == "__main__":
    main()