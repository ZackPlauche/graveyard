# AWS Template Auto
## Description
https://python-forum.io/thread-34144-post-144110.html#pid144110

## Misc Notes
Get VARS-

Application Name:
- Provided by start file.

Account ID:
- Provided by start file.

ApplicationEnvironment:
- aws organizations describe-account --account-id 9785573661 > account.txt (Env found in account friendly name) **Need permissions**

Account ARN:
- aws organizations describe-account --account-id 9785573661 > account.txt (Env found in account ARN) **Need permissions**

VPC ID's:
- aws ec2 describe-vpcs > vpcs.txt (VPC ID's for DMZ [Find "Key: Name/n Value : DMZ/n VPCID: {copy value}],PROMPT to add VPC ID for Internal [Find "Key: Name/n Value : Internal/n VPCID: {copy value}])

Subnets:
- aws ec2 describe-subnets > subnets.txt (Subnet ID's for DMZ [Find "SubnetID: {copy value}/n Key: Name/n Value : DMZ_A"],[Find "SubnetID: {copy value}/n Key: Name/n Value : DMZ_B"])

Security Groups:
