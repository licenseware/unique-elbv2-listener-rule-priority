# Unique ELBv2 Listener Rule Priority

Without any conflict, generate random priotity for a Elastic Load Balancer
Listener Rule.

## Usage

### Prerequisites

For each kind of run, you will need to configure the credentials first, so
consider adding the following step before each of the below approaches:

```yaml
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.REGION }}
```

### Produce only one priority

```yaml
      - uses: licenseware/unique-elbv2-listener-rule-priority@v1
        name: Get unique listerner rule priority
        id: elb-priority
        with:
          listener-arn: ${{ secrets.LOAD_BALANCER_LISTENER_ARN }}

      - uses: aws-actions/aws-cloudformation-github-deploy@v1
        with:
          name: sample-elb-priority
          template: cloudformation-templates/myapp-dev.yml
          no-fail-on-empty-changeset: "1"
          role-arn: ${{ secrets.CLOUD_FORMATION_ROLE_ARN }}
          parameter-overrides: >-
            MyAppLBPriority=${{ steps.elb-priority.outputs.prioritties }}
```

### Produce multiple priorities

```yaml
      - uses: licenseware/unique-elbv2-listener-rule-priority@v1
        name: Get unique listerner rule priority
        id: elb-priority
        with:
          listener-arn: ${{ secrets.LOAD_BALANCER_LISTENER_ARN }}
          sorted: true
          delimiter: " "
          count: 3

      - name: Get load balancer priorities
        run: |
          export PRIORITIES=${{ steps.elb-priority.outputs.prioritties }}

          cat << EOF >> $GITHUB_ENV
          MYAPP_LB_PR=$(echo $SORTED | awk '{print $1}')
          YOURAPP_LB_PR=$(echo $SORTED | awk '{print $2}')
          HISAPP_LB_PR=$(echo $SORTED | awk '{print $3}')
          EOF

      - uses: aws-actions/aws-cloudformation-github-deploy@v1
        with:
          name: sample-elb-priority
          template: cloudformation-templates/myapp-dev.yml
          no-fail-on-empty-changeset: "1"
          role-arn: ${{ secrets.CLOUD_FORMATION_ROLE_ARN }}
          parameter-overrides: >-
            MyAppLBPriority=${{ env.MYAPP_LB_PR }},
            YourAppLBPriority=${{ env.YOURAPP_LB_PR }},
            HisAppLBPriority=${{ env.HISAPP_LB_PR }}
```

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| listener-arn | The ARN of the ELBv2 Listener to generate the priority for. | true |
| count | The number of priorities to generate. | false | 1 |
| min-priority | The minimum priority to use. | false | 1 |
| max-priority | The maximum priority to use. | false | 50000 |
| max-try | The maximum number of tries to generate a unique priority. | false | 10000 |
| log-level | The log level to use. | false | error |
| sorted | Whether to sort the resulting priorities. | false | true |
| delimiter | The delimiter to use on the resulting the priorities. | false | " " |

## Outputs

| Name | Description | Example |
|------|-------------|---------|
| prioritties | Comma-separated list of generated priorities. | 1,2,3 |
