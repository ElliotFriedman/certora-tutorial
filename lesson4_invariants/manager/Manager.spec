
/*
A manager is simply an address

A fund is identified by uint256 fundId
Every fund must have a unique manager

To change managers:

the current manager must set their successor as the pending manager
the pending manager must then claim management using the claimManagement method

Exercises
In the folder manager are three implementations of the IManager interface. One correct implementation and two buggy implementations.

Write an invariant verifying that no two funds have the same manager
Make sure your invariant is sound, remember using requireInvariant in preserved blocks is sound (provided you also prove the required invariant), see Invariants and induction
Test your invariant by running it on the implementations and finding the bugs
*/

methods {
  /// @return whether `manager` currently manages a fund
  function isActiveManager(address manager) external returns bool envfree;

  /// @notice Create a new managed fund setting message sender as its manager
  /// @dev The message sender may not manage another fund
  /// @param fundId the id number of the new fund
  function createFund(uint256 fundId) external;

  /// @notice Set the pending manager for a fund
  /// @dev Only the fund's manager may set the pending manager
  function setPendingManager(uint256 fundId, address pending) external;

  /// @notice Claim management of the fund
  /// @dev Only the pending manager may claim management
  /// @dev The pending manager will become the new current manager of the fund
  function claimManagement(uint256 fundId) external;

  /// @return The current manager of the fund
  function getCurrentManager(uint256 fundId) external returns address envfree;

  /// @return The fund's pending manager
  function getPendingManager(uint256 fundId) external returns address envfree;
}

/// if current manager, must be active
invariant ifCurrentManagerMustBeActive(uint256 fundId)
    (getCurrentManager(fundId) != 0) => (isActiveManager(getCurrentManager(fundId))) {
        preserved claimManagement(uint256 claimedFundId) with (env e) {
            requireInvariant noFundsHaveSameManagers(fundId, claimedFundId);
        }
    }

invariant noFundsHaveSameManagers(uint256 fundIdA, uint256 fundIdB)
    /// first ensure managers exist for funds
    /// and that the funds are not the same. if both of these are true, then
    ((getCurrentManager(fundIdA) != 0) && (getCurrentManager(fundIdB) != 0) && (fundIdA != fundIdB)) =>
    /// the current manager of fund a should not be the current manager of fund b
    (getCurrentManager(fundIdA) != getCurrentManager(fundIdB)) {
        preserved {
            requireInvariant ifCurrentManagerMustBeActive(fundIdA);
            requireInvariant ifCurrentManagerMustBeActive(fundIdB);
        }
    }
