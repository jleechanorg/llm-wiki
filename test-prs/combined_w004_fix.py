# Combined Technique Fix: WA-004 (CI-aware schema prompt, PR #6269)
# Meta-Harness + ExtendedThinking + SWE-bench

import re


# New regex pattern that matches [approve] anywhere in the comment body
CR_APPROVE_PATTERN = r"\[approve\]"


def check_approval_formal(reviews: list) -> bool:
    """
    Check for formal APPROVED review state.

    Args:
        reviews: List of review dicts with 'state' field

    Returns:
        True if any review has state='APPROVED'
    """
    return any(r.get('state') == 'APPROVED' for r in reviews)


def check_approval_cr_fallback(reviews: list, cr_status: str) -> bool:
    """
    Check CR fallback: success status + [approve] comment anywhere.

    Args:
        reviews: List of review dicts
        cr_status: CodeRabbit status ('success' or other)

    Returns:
        True if CR success and [approve] found in CR comment
    """
    if cr_status != 'success':
        return False
    return any(
        bool(re.search(CR_APPROVE_PATTERN, r.get('body', '').lower()))
        for r in reviews
        if r.get('user', '').startswith('coderabbit')
    )


def is_approved(reviews: list, cr_status: str = 'unknown') -> bool:
    """
    Dual-condition approval detection.

    Args:
        reviews: List of review dicts
        cr_status: CodeRabbit status (default 'unknown')

    Returns:
        True if formally approved OR CR fallback approved
    """
    return check_approval_formal(reviews) or check_approval_cr_fallback(reviews, cr_status)


# ============ TESTS ============

def test_cr_approve_regex_matches_anywhere():
    """Test CR approval comment regex matches anywhere, not just line start"""
    cr_comment_exact = "    [approve]"
    cr_comment_inline = "This looks good, [approve] from me!"

    assert re.search(CR_APPROVE_PATTERN, cr_comment_exact), "Should match exact"
    assert re.search(CR_APPROVE_PATTERN, cr_comment_inline), "Should match inline"


def test_dual_condition_approval_detection():
    """Test dual-condition fallback: APPROVED review OR CR [approve] comment"""
    # Case 1: Formal approval exists
    reviews_formal = [{'state': 'APPROVED', 'user': 'reviewer'}]
    assert check_approval_formal(reviews_formal)

    # Case 2: No formal approval but CR [approve] comment
    reviews_cr = [{'body': 'LGTM [approve]', 'user': 'coderabbitai[bot]'}]
    assert check_approval_cr_fallback(reviews_cr, 'success')

    # Case 3: No approval at all
    reviews_none = [{'body': 'Comment', 'user': 'reviewer'}]
    assert not check_approval_formal(reviews_none)
    assert not check_approval_cr_fallback(reviews_none, 'success')


if __name__ == "__main__":
    test_cr_approve_regex_matches_anywhere()
    test_dual_condition_approval_detection()
    print("✓ All WA-004 fix tests passed")