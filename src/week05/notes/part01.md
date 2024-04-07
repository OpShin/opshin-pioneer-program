<!-- [NOTES TO PRESENTER]
Just a short intro lecture. While talking about the stuff below, the presenter can show imgs/utxo_diagram.png on the screen.
-->

# Introduction

In this lecture, we're looking into native tokens on Cardano and how to interact with them in OpShin. Specifically, we'll explore how to construct minting policies that govern the conditions under which native tokens can be minted or burnt.

![image](imgs/utxo_diagram.png)

To lay the groundwork for understanding native tokens, it's essential to revisit the concept of "value" in Cardano. Recall our discussions on the extended UTXO model, where we outlined that each unspent transaction output (UTxO) on the Cardano blockchain is characterized by an address and a value. Additionally, with the extended UTxO model, a datum has become part of a UTxO, as illustrated through various examples in our previous lectures.

Up until now, our focus has predominantly been on Ada (or Lovelace as its smallest unit) when talking about "value" on the blockchain. It's crucial to note that Cardano initially only accommodates Ada (or Lovalace). The creation and elimination of native tokens requires explicit actions: they must be purposely minted when needed and similarly, burnt when they are no longer required. The forthcoming sections of this lecture will delve into the mechanisms of minting and burning native tokens and how to handle/validate these processes in OpShin.