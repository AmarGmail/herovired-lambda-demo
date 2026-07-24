import boto3
import os
from datetime import datetime, timezone, timedelta

# ─── Configuration ─────────────────────────────────────────
VOLUME_ID = os.environ.get('VOLUME_ID')
# add a volume id inline for testing
# VOLUME_ID = 'vol-09a9b73a4ef8086aa'
RETENTION_DAYS = int(os.environ.get('RETENTION_DAYS', 30))
# For testing snapshot deletion ater 30 mins
# RETENTION_MINS = 30
BACKUP_TAG_KEY = 'CreatedBy'
BACKUP_TAG_VALUE = 'Lambda-Backup'

ec2 = boto3.client('ec2')

def create_snapshot(volume_id):
    """
    Creates a snapshot of the specified EBS volume.
    Returns the new snapshot ID.
    """
    if not volume_id: 
        raise ValueError("Environment variable VOLUME_ID is not set.")
    
    print(f"Creating snapshot for volume: {volume_id}")
    response = ec2.create_snapshot(
        VolumeId=volume_id,
        Description=f"Automated backup by Lambda | {datetime.now(timezone.utc).isoformat()}"
    )
    snapshot_id = response['SnapshotId']
    print(f"Created snapshot: {snapshot_id}")
    return snapshot_id

def tag_snapshot(snapshot_id):
    """
    Tags the snapshot with backup metadata.
    """
    ec2.create_tags(
        Resources=[snapshot_id],
        Tags=[
            {"Key": BACKUP_TAG_KEY, "Value": BACKUP_TAG_VALUE},
            {"Key": "VolumeId", "Value": VOLUME_ID},
            {"Key": "CreatedAt", "Value": datetime.now(timezone.utc).isoformat()},
        ],
    )

    print(
        f"Tagged snapshot {snapshot_id} "
        f"with {BACKUP_TAG_KEY}={BACKUP_TAG_VALUE}"
    )

def cleanup_old_snapshots(cutoff_time):
    """
    Deletes snapshots tagged with CreatedBy=Lambda-Backup older than cutoff_time.
    Returns a list of deleted snapshot IDs.
    """
    print(f"Searching for snapshots older than cutoff with tag {BACKUP_TAG_KEY}={BACKUP_TAG_VALUE}")

    account_id = boto3.client('sts').get_caller_identity()['Account']
    deleted = []
    paginator = ec2.get_paginator('describe_snapshots')
    page_iterator = paginator.paginate(
        Filters=[
            {'Name': 'tag:' + BACKUP_TAG_KEY, 'Values': [BACKUP_TAG_VALUE]},
            {'Name': 'owner-id', 'Values': [account_id]}
        ]
    )

    for page in page_iterator:
        for snapshot in page.get('Snapshots', []):
            start_time = snapshot['StartTime']

            if start_time < cutoff_time:
                snap_id = snapshot['SnapshotId']
                try:
                    ec2.delete_snapshot(SnapshotId=snap_id)
                    print(f"Deleted snapshot: {snap_id} (StartTime: {start_time.isoformat()})")
                    deleted.append(snap_id)
                except Exception as e:
                    print(f"ERROR deleting snapshot {snap_id}: {e}")

    return deleted

def lambda_handler(event, context):    
    # Orchestrates snapshot creation, tagging, and cleanup.
    # for testing used minutes with timedelta
    #cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=RETENTION_MINS)
    cutoff_time = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)

    # Step 1: Create
    snapshot_id = create_snapshot(VOLUME_ID)

    # Step 2: Tag
    tag_snapshot(snapshot_id)

     # Step 3: Cleanup
    deleted = cleanup_old_snapshots(cutoff_time)

    # Summary
    print("=" * 50)
    print(f"Created snapshot: {snapshot_id}")
    print(f"Deleted snapshots ({len(deleted)}): {deleted}")
    print("=" * 50)

    return {
        'statusCode': 200,
        'body': {
            'created_snapshot_id': snapshot_id,
            'deleted_snapshot_ids': deleted,
            'deleted_count': len(deleted)
        }
    }