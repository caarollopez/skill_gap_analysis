from collections import Counter
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def compute_skill_gap(rows, user_skills, skill_levels=None):
    """
    Compute skill gap considering user skills and optionally their levels.
    
    Args:
        rows: List of job dictionaries with 'skills_detected' key
        user_skills: Set or list of skills the user has
        skill_levels: Dict mapping skill -> level (can be numeric 1-4 or string: "Basic", "Intermediate", "Advanced", "Expert")
    
    Returns:
        Tuple of (rows with match metrics, missing skills list)
    """
    user_skills = set(user_skills) if user_skills else set()
    skill_levels = skill_levels or {}
    
    # Map string level names to numeric values (for backward compatibility with numeric 1-4)
    level_name_to_numeric = {
        "Basic": 1,
        "Intermediate": 2,
        "Advanced": 3,
        "Expert": 4
    }
    
    def get_numeric_level(skill):
        """Convert skill level to numeric (1-4). Handles both string and numeric inputs."""
        level = skill_levels.get(skill, None)
        if level is None:
            return 4  # Default to Expert (4) if not specified
        # If it's already a number (1-4), return it
        if isinstance(level, (int, float)):
            return int(level)
        # If it's a string, convert using mapping
        if isinstance(level, str):
            return level_name_to_numeric.get(level, 4)  # Default to Expert if unknown string
        return 4  # Fallback to Expert
    
    # Default numeric level is 4 (Expert) if skill is present but no level specified
    default_numeric_level = 4

    for row in rows:
        job_sk = set(row["skills_detected"])
        row["n_skills_job"] = len(job_sk)
        
        # Count skills user has (binary)
        row["n_skills_user_has"] = len(job_sk & user_skills)
        
        # Calculate weighted match considering skill levels
        # Skills with higher levels contribute more to the match
        weighted_match = 0.0
        total_weight = 0.0
        
        for skill in job_sk:
            if skill in user_skills:
                # User has the skill - weight by level (1-4, normalized to 0.25-1.0)
                user_level_numeric = get_numeric_level(skill)
                weight = user_level_numeric / 4.0  # Normalize to 0.25-1.0
                weighted_match += weight
                total_weight += 1.0
            else:
                # User doesn't have the skill
                total_weight += 1.0
        
        # Match ratio: binary (original)
        row["match_ratio"] = (
            row["n_skills_user_has"] / row["n_skills_job"]
            if row["n_skills_job"] > 0 else 0
        )
        
        # Weighted match ratio: considers skill levels
        row["weighted_match_ratio"] = (
            weighted_match / total_weight if total_weight > 0 else 0
        )
        
        # Average level of matched skills (numeric 1-4)
        matched_levels = [get_numeric_level(skill) 
                         for skill in job_sk if skill in user_skills]
        row["avg_skill_level"] = (
            sum(matched_levels) / len(matched_levels) 
            if matched_levels else 0
        )

    all_skills = []
    for row in rows:
        all_skills.extend(row["skills_detected"])

    freq = Counter(all_skills)

    missing = [
        {
            "skill": skill,
            "count": count,
            "priority": count
        }
        for skill, count in freq.most_common()
        if skill not in user_skills
    ]

    return rows, missing


def cluster_jobs(jobs_df: pd.DataFrame, n_clusters: int = 4, random_state: int = 42) -> pd.DataFrame:
    """
    Cluster jobs based on their skill vectors using k-means.
    
    Args:
        jobs_df: DataFrame with 'job_id' and 'skills_detected' columns
        n_clusters: Number of clusters (default: 4)
        random_state: Random seed for reproducibility
        
    Returns:
        DataFrame with added 'cluster' column
    """
    if len(jobs_df) < n_clusters:
        # Not enough jobs for clustering
        jobs_df = jobs_df.copy()
        jobs_df["cluster"] = 0
        return jobs_df
    
    # Get all unique skills
    all_skills = set()
    for skills in jobs_df["skills_detected"]:
        if isinstance(skills, list):
            all_skills.update(skills)
        elif isinstance(skills, str):
            all_skills.update([s.strip() for s in skills.split(",") if s.strip()])
    
    all_skills = sorted(list(all_skills))
    
    if len(all_skills) == 0:
        # No skills found
        jobs_df = jobs_df.copy()
        jobs_df["cluster"] = 0
        return jobs_df
    
    # Create binary matrix: jobs × skills
    matrix = []
    job_ids = []
    
    for _, row in jobs_df.iterrows():
        job_id = row.get("job_id", "")
        skills = row.get("skills_detected", [])
        
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(",") if s.strip()]
        elif not isinstance(skills, list):
            skills = []
        
        skill_set = set(skills)
        vector = [1 if skill in skill_set else 0 for skill in all_skills]
        matrix.append(vector)
        job_ids.append(job_id)
    
    matrix = np.array(matrix)
    
    # Apply k-means
    if matrix.shape[1] > 0:
        # Standardize features (optional, but can help)
        scaler = StandardScaler()
        matrix_scaled = scaler.fit_transform(matrix)
        
        kmeans = KMeans(n_clusters=min(n_clusters, len(jobs_df)), random_state=random_state, n_init=10)
        clusters = kmeans.fit_predict(matrix_scaled)
    else:
        clusters = np.zeros(len(jobs_df), dtype=int)
    
    # Add cluster column
    result_df = jobs_df.copy()
    result_df["cluster"] = clusters
    
    return result_df


def interpret_clusters(jobs_df: pd.DataFrame) -> pd.DataFrame:
    """
    Interpret clusters by finding most common skills in each cluster.
    
    Args:
        jobs_df: DataFrame with 'cluster' and 'skills_detected' columns
        
    Returns:
        DataFrame with cluster interpretations
    """
    cluster_summaries = []
    
    for cluster_id in sorted(jobs_df["cluster"].unique()):
        cluster_jobs = jobs_df[jobs_df["cluster"] == cluster_id]
        
        # Count skills in this cluster
        all_skills = []
        for skills in cluster_jobs["skills_detected"]:
            if isinstance(skills, list):
                all_skills.extend(skills)
            elif isinstance(skills, str):
                all_skills.extend([s.strip() for s in skills.split(",") if s.strip()])
        
        skill_freq = Counter(all_skills)
        top_skills = [skill for skill, _ in skill_freq.most_common(5)]
        
        cluster_summaries.append({
            "cluster": cluster_id,
            "num_jobs": len(cluster_jobs),
            "top_skills": ", ".join(top_skills),
            "avg_match_ratio": cluster_jobs["match_ratio"].mean() if "match_ratio" in cluster_jobs.columns else 0
        })
    
    return pd.DataFrame(cluster_summaries)
