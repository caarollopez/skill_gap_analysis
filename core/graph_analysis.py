"""
Graph analysis module for skill gap analysis.
Implements bipartite graphs, skill co-occurrence networks, centrality measures,
and community detection.
"""
import networkx as nx
import pandas as pd
from collections import Counter
from typing import Dict, List, Tuple, Optional


def build_bipartite_graph(jobs_df: pd.DataFrame) -> nx.Graph:
    """
    Build a bipartite graph connecting jobs to skills.
    
    Args:
        jobs_df: DataFrame with columns 'job_id' and 'skills_detected'
        
    Returns:
        NetworkX bipartite graph
    """
    B = nx.Graph()
    
    # Add nodes with node_type attribute
    for _, row in jobs_df.iterrows():
        job_id = str(row.get("job_id", ""))
        if job_id:
            B.add_node(job_id, node_type="job")
            
            skills = row.get("skills_detected", [])
            if isinstance(skills, str):
                # Handle case where skills might be stored as string
                skills = [s.strip() for s in skills.split(",") if s.strip()]
            elif not isinstance(skills, list):
                skills = []
            
            for skill in skills:
                if skill:
                    B.add_node(skill, node_type="skill")
                    B.add_edge(job_id, skill)
    
    return B


def build_skill_cooccurrence_graph(jobs_df: pd.DataFrame) -> nx.Graph:
    """
    Build a skill co-occurrence graph (projection of bipartite graph).
    Two skills are connected if they appear together in at least one job.
    Edge weight = number of jobs where both skills co-occur.
    
    Args:
        jobs_df: DataFrame with columns 'job_id' and 'skills_detected'
        
    Returns:
        NetworkX weighted graph of skills
    """
    G = nx.Graph()
    
    # Count co-occurrences
    cooccurrence = Counter()
    
    for _, row in jobs_df.iterrows():
        skills = row.get("skills_detected", [])
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(",") if s.strip()]
        elif not isinstance(skills, list):
            skills = []
        
        # Remove duplicates and filter empty
        skills = list(set([s for s in skills if s]))
        
        # Count pairs
        for i, skill1 in enumerate(skills):
            for skill2 in skills[i+1:]:
                pair = tuple(sorted([skill1, skill2]))
                cooccurrence[pair] += 1
    
    # Add edges with weights
    for (skill1, skill2), weight in cooccurrence.items():
        G.add_edge(skill1, skill2, weight=weight)
    
    return G


def compute_centralities(graph: nx.Graph) -> pd.DataFrame:
    """
    Compute various centrality measures for nodes in the graph.
    
    Args:
        graph: NetworkX graph
        
    Returns:
        DataFrame with columns: node, degree, betweenness, closeness, eigenvector
    """
    if len(graph.nodes()) == 0:
        return pd.DataFrame(columns=["node", "degree", "betweenness", "closeness", "eigenvector"])
    
    # Degree centrality
    degree_cent = nx.degree_centrality(graph)
    
    # Check if graph has weighted edges
    has_weights = False
    if graph.number_of_edges() > 0:
        # Check if any edge has a weight attribute
        sample_edge = list(graph.edges(data=True))[0]
        has_weights = "weight" in sample_edge[2] if len(sample_edge) > 2 else False
    
    # Betweenness centrality (only if graph has edges)
    if graph.number_of_edges() > 0:
        try:
            betweenness_cent = nx.betweenness_centrality(graph, weight="weight" if has_weights else None)
        except:
            betweenness_cent = nx.betweenness_centrality(graph)
    else:
        betweenness_cent = {node: 0.0 for node in graph.nodes()}
    
    # Closeness centrality (only for connected graphs)
    try:
        closeness_cent = nx.closeness_centrality(graph, distance="weight" if has_weights else None)
    except:
        try:
            closeness_cent = nx.closeness_centrality(graph)
        except:
            closeness_cent = {node: 0.0 for node in graph.nodes()}
    
    # Eigenvector centrality (only if graph has edges)
    try:
        eigenvector_cent = nx.eigenvector_centrality(graph, weight="weight" if has_weights else None, max_iter=1000)
    except:
        try:
            eigenvector_cent = nx.eigenvector_centrality(graph, max_iter=1000)
        except:
            eigenvector_cent = {node: 0.0 for node in graph.nodes()}
    
    # Weighted degree (sum of edge weights)
    if has_weights:
        weighted_degree = dict(graph.degree(weight="weight"))
    else:
        weighted_degree = dict(graph.degree())
    
    # Combine into DataFrame
    nodes = list(graph.nodes())
    data = {
        "node": nodes,
        "degree": [degree_cent.get(n, 0) for n in nodes],
        "betweenness": [betweenness_cent.get(n, 0) for n in nodes],
        "closeness": [closeness_cent.get(n, 0) for n in nodes],
        "eigenvector": [eigenvector_cent.get(n, 0) for n in nodes],
        "weighted_degree": [weighted_degree.get(n, 0) for n in nodes],
    }
    
    return pd.DataFrame(data).sort_values("degree", ascending=False)


def detect_communities(graph: nx.Graph, algorithm: str = "louvain") -> Dict[str, int]:
    """
    Detect communities in the graph using Louvain algorithm.
    
    Args:
        graph: NetworkX graph
        algorithm: 'louvain' or 'greedy_modularity'
        
    Returns:
        Dictionary mapping node -> community_id
    """
    if len(graph.nodes()) == 0 or graph.number_of_edges() == 0:
        return {node: 0 for node in graph.nodes()}
    
    try:
        if algorithm == "louvain":
            # Try to use python-louvain if available, otherwise use greedy_modularity
            try:
                import community.community_louvain as community_louvain
                communities = community_louvain.best_partition(graph, weight="weight" if graph.is_weighted() else None)
            except ImportError:
                # Fallback to greedy_modularity
                communities_generator = nx.community.greedy_modularity_communities(
                    graph, weight="weight" if graph.is_weighted() else None
                )
                communities = {}
                for i, comm in enumerate(communities_generator):
                    for node in comm:
                        communities[node] = i
        else:
            # Greedy modularity
            communities_generator = nx.community.greedy_modularity_communities(
                graph, weight="weight" if graph.is_weighted() else None
            )
            communities = {}
            for i, comm in enumerate(communities_generator):
                for node in comm:
                    communities[node] = i
    except Exception as e:
        # If community detection fails, assign each node to its own community
        communities = {node: i for i, node in enumerate(graph.nodes())}
    
    return communities


def get_skill_network_metrics(jobs_df: pd.DataFrame) -> Tuple[nx.Graph, pd.DataFrame, Dict[str, int]]:
    """
    Compute complete skill network analysis: graph, centralities, and communities.
    
    Args:
        jobs_df: DataFrame with job data and skills_detected column
        
    Returns:
        Tuple of (cooccurrence_graph, centralities_df, communities_dict)
    """
    # Build co-occurrence graph
    graph = build_skill_cooccurrence_graph(jobs_df)
    
    # Compute centralities
    centralities = compute_centralities(graph)
    
    # Detect communities
    communities = detect_communities(graph)
    
    return graph, centralities, communities


def get_bridge_skills(centralities_df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Identify bridge skills (high betweenness centrality).
    These are skills that connect different communities.
    
    Args:
        centralities_df: DataFrame from compute_centralities()
        top_n: Number of top bridge skills to return
        
    Returns:
        DataFrame with top bridge skills
    """
    if "betweenness" not in centralities_df.columns:
        return pd.DataFrame()
    
    bridge_skills = centralities_df.nlargest(top_n, "betweenness")
    return bridge_skills[["node", "betweenness", "degree"]]

