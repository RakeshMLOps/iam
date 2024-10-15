import boto3
import csv

# Initialize the IAM client
iam_client = boto3.client('iam')

# Define the prefix to filter roles and policies by (replace with your desired prefix)
prefix = "your-prefix-here"

# List IAM roles
roles_response = iam_client.list_roles()

# Filter roles that start with the specified prefix
filtered_roles = [role['RoleName'] for role in roles_response['Roles'] if role['RoleName'].startswith(prefix)]

# Prepare a list to hold CSV data (headers: RoleName, PolicyName, Action)
csv_data = [["RoleName", "PolicyName", "Action"]]

if filtered_roles:
    print(f"IAM Roles that start with prefix '{prefix}':\n")

    for role_name in filtered_roles:
        print(f"Role: {role_name}")
        
        # List attached role policies
        attached_policies_response = iam_client.list_attached_role_policies(RoleName=role_name)
        attached_policies = attached_policies_response['AttachedPolicies']
        
        # Use a set to ensure unique policies
        unique_policies = set()
        
        for policy in attached_policies:
            policy_arn = policy['PolicyArn']
            policy_name = policy['PolicyName']
            
            # Check for duplicates
            if policy_arn not in unique_policies:
                unique_policies.add(policy_arn)
                print(f"  Policy: {policy_name}")
                
                # Get the policy details
                policy_version_response = iam_client.get_policy(PolicyArn=policy_arn)
                policy_version = policy_version_response['Policy']['DefaultVersionId']
                
                # Get the policy document for the default version
                policy_document_response = iam_client.get_policy_version(
                    PolicyArn=policy_arn,
                    VersionId=policy_version
                )
                
                policy_document = policy_document_response['PolicyVersion']['Document']
                statements = policy_document.get('Statement', [])
                
                # Use a set to store and remove duplicate actions
                unique_actions = set()
                
                # Loop through policy statements
                for statement in statements:
                    actions = statement.get('Action', [])
                    
                    # Ensure actions are a list
                    if not isinstance(actions, list):
                        actions = [actions]
                    
                    # Add actions to the set, filtering duplicates
                    for action in actions:
                        if action not in unique_actions:
                            unique_actions.add(action)
                            print(f"    Action: {action}")
                            
                            # Append the role, policy, and action to the CSV data list
                            csv_data.append([role_name, policy_name, action])
        print("\n")
else:
    print(f"No IAM roles found starting with '{prefix}'.")

# Save to a CSV file
csv_filename = "iam_roles_policies_actions.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)

print(f"Data successfully written to {csv_filename}")
