# PatternMiner

## About PatternMiner
**PatternMiner** is a set of Python 3 tools for conducting pattern analysis, clustering, and data mining based, in part, on some of the methods described in the Coursera course “Pattern Discovery in Data Mining”. The aim of this project is to add implementations of the algorithms listed below so that other researchers, learners, and enthusiasts have the tools easily available to them. 

## Using PatternMiner

Using **PatternMiner** is easy.  Currently, the *Apriori* algorithm is implemented and supported, and to use the *Apriori* algorithm we simply need to instantiate the **_Apriori_** class and feed it data via the `bulkAdd()` method (here we have a file named _transactions.txt_ which has transactions, one per line, with items separated by a **;**):

```
import PatternMiner as pm
ap_miner = pm.Apriori()
ap_miner.bulkAdd([l.strip().split(';') for l in open('transactions.txt','r')])
```

Now that we have loaded data into our miner, we can construct all of the _lenght-k_ sets that exist with a supplied support, such as 500 in the example below.  **Note: we can create as many _length-k_ supported sets as our memory allows**

```
support = 500
ap_miner.kLengthSet(support)
max_k = max(ap_miner.kLengthSets[support].keys())
for item in ap_miner.kLengthSets[support][max_k]['items'].keys():
    print(item, ap_miner.kLengthSets[support][max_k]['items'][item])
```



## Alogrithms to Add

- [x] Apriori 
- [ ] H-Miner
- [ ] FPGrowth
- [ ] ECLAT
