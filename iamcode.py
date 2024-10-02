import boto3
import json

def list_iam_roles_and_policies():
    # Create an IAM client
    iam_client = boto3.client('iam')

    # Initialize a dictionary to hold roles and policies
    roles_and_policies = {}

    # List all roles
    print("Fetching IAM Roles...")
    roles = iam_client.list_roles()
    for role in roles['Roles']:
        role_name = role['RoleName']
        roles_and_policies[role_name] = {
            'RoleArn': role['Arn'],
            'AttachedPolicies': []
        }
        
        # List attached policies for each role
        attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)
        for policy in attached_policies['AttachedPolicies']:
            roles_and_policies[role_name]['AttachedPolicies'].append({
                'PolicyName': policy['PolicyName'],
                'PolicyArn': policy['PolicyArn']
            })

    # Output the roles and policies in JSON format
    with open('iam_roles_and_policies.json', 'w') as json_file:
        json.dump(roles_and_policies, json_file, indent=4)

    print("IAM roles and policies have been saved to 'iam_roles_and_policies.json'.")

if __name__ == "__main__":
    list_iam_roles_and_policies()
