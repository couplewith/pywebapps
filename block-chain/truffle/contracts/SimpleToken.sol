// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleToken {

    mapping(address => uint) private _balances;

    constructor() {
        _balances[msg.sender] = 1000000;
    }

    function getBalance(address account) public view returns (uint) {
        return _balances[account];
    }

    function transfer(address to, uint amount) public {
        require(_balances[msg.sender] >= amount);

        _balances[msg.sender] -= amount;
        _balances[to] += amount;
    }
}

