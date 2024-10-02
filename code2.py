import boto3
import json

def list_iam_roles_and_policies():
    # Create an IAM client
    iam_client = boto3.client('iam')
    
    # List IAM roles
    roles_response = iam_client.list_roles()
    roles = roles_response['Roles']

    roles_with_policies = []

    for role in roles:
        role_name = role['RoleName']
        role_details = {
            'RoleName': role_name,
            'AttachedPolicies': []
        }

        # List attached policies for the role
        policies_response = iam_client.list_attached_role_policies(RoleName=role_name)
        attached_policies = policies_response['AttachedPolicies']

        for policy in attached_policies:
            role_details['AttachedPolicies'].append({
                'PolicyName': policy['PolicyName'],
                'PolicyArn': policy['PolicyArn']
            })

        roles_with_policies.append(role_details)

    return json.dumps(roles_with_policies, indent=4)

if __name__ == "__main__":
    roles_json = list_iam_roles_and_policies()
    print(roles_json)
