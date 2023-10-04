
methods {
    function highestBidder() external returns address envfree;
    function highestBid() external returns uint256 envfree;
    function seller() external returns address envfree;
    function bids(address) external returns uint256 envfree;
    function operators(address, address) external returns bool envfree;
    function MINIMUM_BID() external returns uint256 envfree;
}

/// The highestBid is higher or equal to any other bid.

/// highest bid cannot be less than c's bid
invariant validInitialState(address c)
    highestBid() >= bids(c);

/// highest bidder must have highest bid and bid must be equal to highest bid
invariant highestBidderIsHighest(address highest)
    ((highestBidder() != 0) && (highestBidder() == highest)) => (bids(highest) == highestBid());

/// 
invariant highestBidInvariantForAll(address c)
    (((c != highestBidder() && hasBid) => (bids(c) < highestBid()))) {
        preserved {
            requireInvariant validInitialState(c);
        } preserved withdraw() with (env e) {
            requireInvariant highestBidInvariantForAll(e.msg.sender);
        } preserved withdrawAmount(address recipient, uint256 amount) with (env e) {
            requireInvariant highestBidInvariantForAll(e.msg.sender);
        } preserved withdrawFor(address bidder, uint256 amount) with (env e) {
            requireInvariant highestBidInvariantForAll(e.msg.sender);
        }
    }

invariant highestBidGreaterThanMinBid(address a)
    hasBid => highestBid() > MINIMUM_BID() {
        preserved {
            requireInvariant validInitialState(a);
            requireInvariant highestBidderIsHighest(a);
        }
    }

ghost bool hasBid {
    init_state axiom hasBid == false;
}

hook Sstore bids[KEY address a] uint256 new_val (uint256 old_val) STORAGE {
  hasBid = true;
}
