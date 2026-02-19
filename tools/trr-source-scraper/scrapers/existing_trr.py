"""
Scanner for finding existing TRRs related to a technique.
"""

import re
from pathlib import Path
from typing import Dict, Optional, List, Tuple
import json


class ExistingTRRScanner:
    """
    Scans the Completed TRRs directory for existing reports related to a technique.
    """
    
    def __init__(self, trr_directory: Optional[Path] = None):
        """
        Initialize the scanner.
        
        Args:
            trr_directory: Path to Completed TRRs directory. If None, will try to
                          find it relative to this script's location.
        """
        if trr_directory is None:
            # Try to find the Completed TRRs directory
            script_dir = Path(__file__).parent
            project_root = script_dir.parent.parent.parent  # Go up to Tired Labs
            trr_directory = project_root / "Completed TRRs"
        
        self.trr_directory = Path(trr_directory)
    
    def find_related_trrs(self, technique_id: str, technique_name: str = "") -> List[Dict]:
        """
        Find existing TRRs that match or relate to the given technique.
        
        Args:
            technique_id: MITRE ATT&CK technique ID (e.g., T1003.006)
            technique_name: Human-readable technique name for fuzzy matching
            
        Returns:
            List of dictionaries with TRR information
        """
        if not self.trr_directory.exists():
            return []
        
        related_trrs = []
        technique_id = technique_id.upper().strip()
        
        # Normalize technique ID for comparison
        parent_id = technique_id.split('.')[0] if '.' in technique_id else technique_id
        
        # Search through markdown files in Completed TRRs
        for trr_file in self.trr_directory.glob("*.md"):
            match_info = self._check_trr_file(trr_file, technique_id, parent_id, technique_name)
            if match_info:
                related_trrs.append(match_info)
        
        return related_trrs
    
    def _check_trr_file(self, file_path: Path, technique_id: str, parent_id: str, technique_name: str) -> Optional[Dict]:
        """
        Check if a TRR file matches the given technique.
        
        Returns:
            Dictionary with TRR info if match found, None otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return None
        
        # Check for exact technique ID match
        technique_pattern = rf'\b{re.escape(technique_id)}\b'
        parent_pattern = rf'\b{re.escape(parent_id)}(?:\.\d+)?\b'
        
        match_type = None
        match_score = 0
        
        # Check for exact match
        if re.search(technique_pattern, content, re.IGNORECASE):
            match_type = 'exact'
            match_score = 100
        # Check for parent technique match
        elif re.search(parent_pattern, content, re.IGNORECASE):
            match_type = 'parent'
            match_score = 75
        # Check for technique name match (fuzzy)
        elif technique_name:
            name_words = technique_name.lower().split()
            content_lower = content.lower()
            word_matches = sum(1 for word in name_words if len(word) > 3 and word in content_lower)
            if word_matches >= min(2, len(name_words)):
                match_type = 'name'
                match_score = 50
        
        if match_type:
            trr_info = {
                'file_path': str(file_path),
                'file_name': file_path.name,
                'match_type': match_type,
                'match_score': match_score,
                'trr_id': self._extract_trr_id(content),
                'techniques': self._extract_technique_ids(content),
                'references': self._extract_references(content),
                'title': self._extract_title(content),
            }
            return trr_info
        
        return None
    
    def _extract_trr_id(self, content: str) -> Optional[str]:
        """Extract TRR ID from content."""
        # Look for TRR ID in metadata or header
        patterns = [
            r'TRR\s*ID[:\s]+(TRR\d+)',
            r'\*\*ID\*\*[:\s]*(TRR\d+)',
            r'\|\s*ID\s*\|\s*(TRR\d+)',
            r'(TRR\d{4})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).upper()
        return None
    
    def _extract_technique_ids(self, content: str) -> List[str]:
        """Extract all MITRE ATT&CK technique IDs from content."""
        # Match T followed by 4 digits, optionally followed by . and 3 more digits
        pattern = r'\b(T\d{4}(?:\.\d{3})?)\b'
        matches = re.findall(pattern, content, re.IGNORECASE)
        return list(set(m.upper() for m in matches))
    
    def _extract_references(self, content: str) -> List[Dict]:
        """Extract references section from TRR content."""
        references = []
        
        # Find the references section
        ref_pattern = r'##\s*References\s*\n(.*?)(?=##|$)'
        match = re.search(ref_pattern, content, re.IGNORECASE | re.DOTALL)
        
        if match:
            ref_section = match.group(1)
            
            # Extract markdown links
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            for link_match in re.finditer(link_pattern, ref_section):
                references.append({
                    'name': link_match.group(1).strip(),
                    'url': link_match.group(2).strip()
                })
            
            # If no markdown links, try to extract plain URLs
            if not references:
                url_pattern = r'https?://[^\s\)]+'
                for url_match in re.finditer(url_pattern, ref_section):
                    references.append({
                        'name': 'Reference',
                        'url': url_match.group(0)
                    })
        
        return references
    
    def _extract_title(self, content: str) -> str:
        """Extract the title from TRR content."""
        # Try to find the first h1 header
        h1_pattern = r'^#\s+(.+)$'
        match = re.search(h1_pattern, content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # Try to extract from filename convention
        return ""
    
    def find_ddm_files(self, technique_id: str) -> List[Dict]:
        """
        Find DDM (Detection Data Model) JSON files related to a technique.
        
        Args:
            technique_id: MITRE ATT&CK technique ID
            
        Returns:
            List of dictionaries with DDM file information
        """
        if not self.trr_directory.exists():
            return []
        
        ddm_files = []
        
        # Check Completed DDMs directory
        ddm_dir = self.trr_directory.parent / "Completed DDMs"
        if ddm_dir.exists():
            for ddm_file in ddm_dir.glob("*.json"):
                try:
                    with open(ddm_file, 'r', encoding='utf-8') as f:
                        ddm_content = json.load(f)
                except:
                    continue
                
                # Check if this DDM relates to the technique
                if self._ddm_matches_technique(ddm_file.name, ddm_content, technique_id):
                    ddm_files.append({
                        'file_path': str(ddm_file),
                        'file_name': ddm_file.name,
                        'technique_id': technique_id,
                    })
        
        return ddm_files
    
    def _ddm_matches_technique(self, filename: str, content: Dict, technique_id: str) -> bool:
        """Check if a DDM file relates to the given technique."""
        # Check filename
        if technique_id.replace('.', '_') in filename:
            return True
        
        # Check content if it has technique references
        content_str = json.dumps(content)
        if technique_id in content_str:
            return True
        
        return False


def scan_for_existing_trrs(
    technique_id: str,
    technique_name: str = "",
    trr_directory: Optional[Path] = None
) -> Tuple[List[Dict], List[Dict]]:
    """
    Convenience function to scan for existing TRRs and DDMs.
    
    Args:
        technique_id: MITRE ATT&CK technique ID
        technique_name: Human-readable technique name
        trr_directory: Path to TRR directory
        
    Returns:
        Tuple of (trrs, ddm_files)
    """
    scanner = ExistingTRRScanner(trr_directory)
    trrs = scanner.find_related_trrs(technique_id, technique_name)
    ddms = scanner.find_ddm_files(technique_id)
    return trrs, ddms