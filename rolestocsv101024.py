import boto3
import csv

def list_iam_roles_and_policies_to_csv(file_name):
    iam_client = boto3.client('iam')

    # Open the CSV file for writing
    with open(file_name, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write the header
        csv_writer.writerow(['RoleName', 'PolicyName', 'PolicyArn', 'Actions'])

        # List all roles
        roles = iam_client.list_roles()
        for role in roles['Roles']:
            role_name = role['RoleName']

            # List policies attached to the role
            attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)
            for policy in attached_policies['AttachedPolicies']:
                policy_arn = policy['PolicyArn']
                policy_name = policy['PolicyName']

                # Get the policy document
                policy_version = iam_client.get_policy(PolicyArn=policy_arn)['Policy']['DefaultVersionId']
                policy_document = iam_client.get_policy_version(
                    PolicyArn=policy_arn,
                    VersionId=policy_version
                )['PolicyVersion']['Document']

                # List actions allowed by the policy
                actions_list = []
                if 'Statement' in policy_document:
                    for statement in policy_document['Statement']:
                        actions = statement.get('Action', [])
                        if isinstance(actions, str):
                            actions = [actions]
                        actions_list.extend(actions)

                # Write to CSV
                for action in actions_list:
                    csv_writer.writerow([role_name, policy_name, policy_arn, action])

if __name__ == "__main__":
    output_file = 'iam_roles_policies.csv'
    list_iam_roles_and_policies_to_csv(output_file)
    print(f'Data has been written to {output_file}')
