import boto3
import json

def list_iam_roles_and_policies():
    # Create an IAM client
    iam_client = boto3.client('iam')

    # Initialize a dictionary to hold roles and policies
    roles_and_policies = {}

    # Paginate through all roles
    paginator = iam_client.get_paginator('list_roles')
    
    print("Fetching IAM Roles...")
    for response in paginator.paginate():
        for role in response['Roles']:
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
    output_file = 'iam_roles_and_policies.json'
    with open(output_file, 'w') as json_file:
        json.dump(roles_and_policies, json_file, indent=4)

    print(f"IAM roles and policies have been saved to '{output_file}'.")

if __name__ == "__main__":
    list_iam_roles_and_policies()
