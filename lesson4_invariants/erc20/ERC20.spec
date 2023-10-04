
/// ERC20 interface

methods {
    function balanceOf(address) external returns uint256 envfree;
    function transfer(address, uint256) external returns bool;
    function transferFrom(address, address, uint256) external returns bool;
    function approve(address, uint256) external returns bool;
    function allowance(address, address) external returns uint256 envfree;
    function _owner() external returns address envfree;
    function totalSupply() external returns uint256 envfree;
    function name() external returns string envfree;
    function symbol() external returns string envfree;
    function decimals() external returns uint8 envfree;
}

invariant AddressZeroNoBalance()
    balanceOf(0) == 0;
