# AWS CHEATSHEET

# EC2 
- EC2 creates VMs with my choice of OS & H/W. 
- Elastic Cloud Compute
- Use as a remote server.
	- Open using the console. 
	- Select AMI (OS), instance (H/w), key/value pair (security), VPC (Virtual Pvt Cloud - optional)
	- Launch the instance.

	## Connecting to WinSCP
	- Copy public dns from console
	- copy default username (ec2-user)
	- go to advanced, copy path of pem key.
	- Connect.

	## Copy file local OS to EC2.
	``` scp -i "path-to-pem-key-local-os" "path/to/local/file"  ec2-user@<public-dns>:~```
	- Here, ~ at the end = root.

	## Copy file from EC2 to local OS.
	``` scp -i "path-to-pem-key-local-os" ec2-user@<public-dns>:"path/to/remote/file" "path/to/local/file"```
	
	## Check out
	- AutoScaling
		- Create a launch template.
		- Create an autoscaling group.
		- Then use that to double the number of ec2 instances.
		- Can be configured with Load balancer optionally.

# File Storage Systems

	## S3
	- Simple Storage Service
		- Use for Blob/backup/archive/long Storage
		- Used to create Data Lake.
		- Unlimited Storage
	
	## EFS
	- Elastic File Systems
		- File Storage - NFS/shared N/w drive.
		- Mounts to Multiple EC2.
		- Low latency & ELASTIC.
		- Shared applications, Content Mgt, Big Data Analytics
		
	## EBS
	- Elastic Block Store
		- Raw unformatted disk drive.
		- Single EC2
		- Lowest latency 
		- Manually scaled.
		- Less Durable, snaps Backed in S3.
		- DB, single instance apps.
		
# IAM
- Identity Access Management
	## User 
	- An individual
		- When created we can setup the username.
	
	## Policy
	- Access to something, eg = View EC2 instances, Admin....
	
	## User group
	- One group with a set of policies
	- Tag user to Policy
	
# CLI
- aws <command> <subcommand> [options and parameters]
	- *aws* : Calls AWS CLI
	- *command* : Specifies AWS Service (Eg - S3, ec2, iam)
	- *subcommand* : Specific operation to perform.
	- *operation & parameters*  : required/optional values.
	
	# Commands
	- Execute in powershell after creating cloudformation stack.
	
	## Version
	- ``` aws --verison```
	
	## Configure region
	- ```aws configure set region us-west-1```
	
	## Login
	- ``` aws login```
	
		## Clear login cache in powershell.
		- Remove-Item -Recurse -Force "$env:USERPROFILE\.aws\sso\cache" -ErrorAction SilentlyContinue
		- Remove-Item -Recurse -Force "$env:USERPROFILE\.aws\cli\cache" -ErrorAction SilentlyContinue
		
		### Remove Item using powershell
		- cd ~\.aws
		- Remove-Item *
		
		## Sample permissions for this account.
		- AmazonEC2FullAccess
		- AmazonECS_FullAccess
		- AmazonS3FullAccess
		- AWSLambda_FullAccess
		- SignInLocalDevelopmentAccess
		
	## Check login info
	- ```aws sts get-caller-identity```
	
	## Store profile info
	- ```aws configure --profile whatever-you-want``` - 
	## View Configured profiles.
	- ```aws configure list-profiles```
	
	## Check EC2 images we own.
	- ```aws ec2 describe-images --owner self```
	
	## SAMPLE 
		### -- Add filters
		- Filters are K:v pairs. Name:Value.
		- Filtering on server
		### -- Specific Query
		- Say we only want the ImageID & Platform details.
		
		## Example shows ec2 imgs, filter, query.
		PS C:\Users\> aws ec2 describe-images --owner amazon
		{
			"Images": [
				{
					"PlatformDetails": "Linux/UNIX",
					"UsageOperation": "RunInstances",
					"BlockDeviceMappings": [
						{
							"Ebs": {
								"DeleteOnTermination": true,
								"SnapshotId": "snap-05ea1179da93c108a",
								"VolumeSize": 8,
								"VolumeType": "gp2",
								"Encrypted": false
							},
							"DeviceName": "/dev/xvda"
						}
					],
					"EnaSupport": true,
					"Hypervisor": "xen",
					"ImageOwnerAlias": "amazon",
					"Name": "aws-elasticbeanstalk-amzn-2.0.20250623.64bit-eb_corretto8_amazon_linux_2-hvm-2025-06-25T16-04-11.870Z",
					"RootDeviceName": "/dev/xvda",
					"RootDeviceType": "ebs",
					"SriovNetSupport": "simple",
					"VirtualizationType": "hvm",
					"DeprecationTime": "2027-06-25T16:10:54.000Z",
					"SourceInstanceId": "i-03b1fc5082dbf9a11",
					"SourceImageId": "ami-0bbe33b61c1e14975",
		PS C:\Users\> aws ec2 describe-images --owner amazon --filters "Name=root-device-type, Values=ebs"
		{
			"Images": [
				{
					"PlatformDetails": "Linux/UNIX",
					"UsageOperation": "RunInstances",
					"BlockDeviceMappings": [
						{
							"Ebs": {
								"DeleteOnTermination": true,
								"SnapshotId": "snap-091cd20656a8ea590",
								"VolumeSize": 4,
								"VolumeType": "gp3",
								"Encrypted": false
							},
							"DeviceName": "/dev/xvda"
						},
						{
							"Ebs": {
								"DeleteOnTermination": true,
								"SnapshotId": "snap-02d2827c7e5c36c9a",
								"VolumeSize": 18,
								"VolumeType": "gp3",
								"Encrypted": false
							},
							"DeviceName": "/dev/xvdb"
						}
					],
					"Description": "bottlerocket-aws-k8s-1.33-nvidia-aarch64-v1.54.0-5043decc",
					"EnaSupport": true,
		PS C:\Users\>
	
	## Limit max number of results.
	- ```aws ec2 describe-images --owner amazon  --max-items 5```
	
	## Output Table instead of json. You can also o/p text.
	- ```aws ec2 describe-images --owner amazon  --output table```
	
	## Create Security groups on EC2.
	- ```aws ec2 create-security-group --group-name <group-name> --description '<my-description>'```
	
	## Add tags to Security group.
	- You need the GroupID 
	- ```aws ec2 create-tags --resources <security group ids > --tags '[{"Key" : "", "Value" : ""}]'```
	- In powershell, use \` as escape character to save "
	
	## Delete Security Group.
	- ``` aws ec2 delete-security-group --group-id <my-group-id>```

# Firewall
	- Operates at layers 3-7
	- Uses Access Control Lists (ACL)
	- Blanket over VPC.
	- Enfore custom rules.
		- Centrally Managed
		- Auto Scales.
		- VPC to VPC security.
	
	## Keywords
		-Firewall policy : How to handle traffic.
		- Rule group :  Inspection rules together.
		- Stateful Rules : Maintain context across multiple packets
		- Stateless Rules : Evaluate each packet (no prev context).
		- Endpoints : Where to inspect traffic.
		- Domain list : Filter.
		- Traffic flow : path of packets.
		- Logging : Logs
		- Rule Actions : Allow/Drop/Alert
		- IPS : intrusion prevention.

# ECS
- Elastic Container Service
	
	## Keywords
		- Containers : Docker
		- Task definitions : JSOn specifying parameters for Containers.
			- Docker images
			- CPU & Memory
			- Port Mappings
			- Env vars
			- Data Volumes
			- Container dependency
			- immutable: no update allowed. create new. 
		- task : one instance of deployment running
		- services : ECS Service scheduler relaunches tasks on fail/stop.
		- Cluster : group of tasks or services.
			- Clusters provide isolation b/w dev/test/prod.
			
		- Launch Type : 
			- EC2 : Cluster of EC2 to run ECS.
			- Fargate : Serverless launch.
			
		- Container Agent : Runs on each container in cluster. Tells ECS about resource usage. Need to manage on EC2.
		
		- Task Placement Strategies : Decide how to terminate tasks (scale in) / place tasks.
			- Bin Pack Strategy : Fewest instances.
			- Random Strategy : Place tasks randomly.
			- Spread Strategy : distribute evenly on x.
			
	# Deployments
	
		# Rolling Updates
		- New tasks started before old ones are stopped.
		
		# AWS CodeDeploy
		- Blue/Green deployments.
		- Deploy new versions alongside old ones before switching traffic.
		- Easy rollbacks.
		
	# Service Discovery
		- AWS ECS uses AWS Cloud Map.
		- Cloud Map allows service Discovery
		- Different containerized services can connect to each other.
	
	# ECR
	- Elastic Container Registry
		- Stores Docker container images. = DockerHub.
		
	# Sample ecs-task.yml
		# ecs-task.yaml
			Resources:
			  MyTask:
				Type: AWS::ECS::TaskDefinition
				Properties:
				  Family: my-app
				  RequiresCompatibilities: [FARGATE]
				  Cpu: 256
				  Memory: 512
				  ContainerDefinitions:
					- Name: app
					  Image: nginx:latest
	# CloudFormation.
	
	- Stack. Creates templates for everything.
	- Infra as code.
	
		## USAGE
			### Create stack
			- aws cloudformation create-stack `
			  --stack-name my-ecs-app `
			  --template-body file://ecs-fargate.yaml `
			  --parameters ParameterKey=EnvVpcId,ParameterValue=vpc-123456 ParameterKey=EnvSubnetIds,ParameterValue=subnet-111111,subnet-222222 `
			  --capabilities CAPABILITY_NAMED_IAM
			
			### Check Status
			aws cloudformation describe-stacks --stack-name my-ecs-app --query 'Stacks[0].StackStatus'
			
			### Update Stack infra.
			
			- aws cloudformation create-stack `
			  --stack-name my-ecs-app `
			  --template-body file://ecs-fargate.yaml `
			  --parameters ParameterKey=EnvVpcId,ParameterValue=vpc-123456 ParameterKey=EnvSubnetIds,ParameterValue=subnet-111111,subnet-222222 `
			  --capabilities CAPABILITY_NAMED_IAM
			  
		## SAMPLE FILE://ECS-FARGATE/yaml
		
			AWSTemplateFormatVersion: '2010-09-09'
			Description: 'Deploy a simple Nginx service on ECS Fargate'

			Parameters:
			  EnvVpcId:
				Type: AWS::EC2::VPC::Id
				Description: VPC ID for the service
			  EnvSubnetIds:
				Type: List<AWS::EC2::Subnet::Id>
				Description: Subnet IDs for the service

			Resources:
			  # 1. Security Group (Firewall)
			  ContainerSecurityGroup:
				Type: AWS::EC2::SecurityGroup
				Properties:
				  GroupDescription: Allow HTTP from ALB
				  VpcId: !Ref EnvVpcId
				  SecurityGroupIngress:
					- IpProtocol: tcp
					  FromPort: 80
					  ToPort: 80
					  CidrIp: 0.0.0.0/0

			  # 2. ECS Cluster
			  ECSCluster:
				Type: AWS::ECS::Cluster
				Properties:
				  ClusterName: MyFargateCluster

			  # 3. Task Execution Role (Allows ECS to pull images/logs)
			  TaskExecutionRole:
				Type: AWS::IAM::Role
				Properties:
				  AssumeRolePolicyDocument:
					Version: '2012-10-17'
					Statement:
					  - Effect: Allow
						Principal:
						  Service: ecs-tasks.amazonaws.com
						Action: sts:AssumeRole
				  ManagedPolicyArns:
					- arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

			  # 4. Task Definition (The Container Blueprint)
			  WebTaskDefinition:
				Type: AWS::ECS::TaskDefinition
				Properties:
				  Family: nginx-task
				  RequiresCompatibilities:
					- FARGATE
				  NetworkMode: awsvpc
				  Cpu: 256
				  Memory: 512
				  ExecutionRoleArn: !GetAtt TaskExecutionRole.Arn
				  ContainerDefinitions:
					- Name: nginx
					  Image: public.ecr.aws/nginx/nginx:latest
					  PortMappings:
						- ContainerPort: 80
						  Protocol: tcp

			  # 5. ECS Service (Runs the Tasks)
			  WebService:
				Type: AWS::ECS::Service
				DependsOn: ContainerSecurityGroup
				Properties:
				  Cluster: !Ref ECSCluster
				  TaskDefinition: !Ref WebTaskDefinition
				  DesiredCount: 1
				  LaunchType: FARGATE
				  NetworkConfiguration:
					AwsvpcConfiguration:
					  AssignPublicIp: ENABLED
					  Subnets: !Ref EnvSubnetIds
					  SecurityGroups:
						- !Ref ContainerSecurityGroup
				
		
	
	
	
# ECS Upload
	- First create a cluster.
	- Default : Keep Cloudwatch off due to some role issue, once the cloudformation stack is created, you can update cloudwatch to yes.
	- Set retention Policy
	
	## Push Docker image to ECR
	
		### Create Repository on ECR.
		- ```aws ecr create-repository --repository-name demo-frontline-frontend-ui```
		- If you fail, create inline permissions on IAM to create-repository.
		
		### Authenticate with ECR.
		
		- ```aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com```
		- Important before pushing image.
		
		###  Tag docker image to aws_account_id.dkr.ecr.region.amazonaws.com/my-repository:tag
		- ``` docker tag MY-DOCKER-IMAGE-NAME aws_account_id.dkr.ecr.region.amazonaws.com/my-repository:tag ```
		- This sets the path where we are pushing the docker image.
		
		### Push to ECR.
		- ```docker push aws_account_id.dkr.ecr.region.amazonaws.com/my-repository:tag ```
		- In both cases, use default tag = "latest" as a version tracker/whatever.
		
		### Verify image sent to ecr.
		- ```aws ecr list-images --repository-name demo-frontline-frontend-ui --output table ```
		
		