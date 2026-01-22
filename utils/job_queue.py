import json
import os
import time
import uuid
from datetime import datetime
import config


def _load_jobs():
    """Load jobs from JSON file."""
    if not os.path.exists(config.JOBS_FILE):
        return []
    
    try:
        with open(config.JOBS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _save_jobs(jobs):
    """Save jobs to JSON file."""
    with open(config.JOBS_FILE, 'w') as f:
        json.dump(jobs, f, indent=2)


def create_job(filepath, filename, page_count, settings, amount, utr=''):
    """Create a new print job."""
    job = {
        'job_id': str(uuid.uuid4())[:8],  # Short unique ID
        'filename': filename,
        'filepath': filepath,
        'page_count': page_count,
        'created_at': datetime.now().isoformat(),
        'settings': settings,
        'amount': amount,
        'utr': utr,
        'status': 'pending'
    }
    
    jobs = _load_jobs()
    jobs.append(job)
    _save_jobs(jobs)
    
    return job['job_id']


def get_job(job_id):
    """Get a job by ID."""
    jobs = _load_jobs()
    for job in jobs:
        if job['job_id'] == job_id:
            return job
    return None


def get_pending_jobs():
    """Get all pending jobs."""
    jobs = _load_jobs()
    return [job for job in jobs if job['status'] == 'pending']


def approve_job(job_id):
    """Mark job as approved."""
    jobs = _load_jobs()
    for job in jobs:
        if job['job_id'] == job_id:
            job['status'] = 'approved'
            _save_jobs(jobs)
            return True
    return False


def mark_printed(job_id):
    """Mark job as printed."""
    jobs = _load_jobs()
    for job in jobs:
        if job['job_id'] == job_id:
            job['status'] = 'printed'
            job['printed_at'] = datetime.now().isoformat()
            _save_jobs(jobs)
            return True
    return False
