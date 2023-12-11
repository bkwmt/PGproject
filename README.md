# PGproject

data (v.2): 80240 pairs. Exclude all output data labeled 'Acoustic guitar' and their input pairs.



## 資料預處理

為了進行吉他破音去效果（de-effect）的研究，我們從 Positive Grid 公司獲得了一筆豐富的數據集。這些數據包括客戶在雲端儲存的以及經過PG公司效果器（plugin）產品處理後的音檔以及未經處理的原始音檔。依據 PG 原本的收集設定，我們將每個音檔精確地切割為四秒長度，形成了 13 萬對成對資料，總計 26 萬個音檔，並將相關信息輸入到 CSV 文件中進行組織和記錄。

面對數據集中混雜的音質和品質，我們採取了一系列的預處理步驟來清理和篩選數據。首先，我們使用了 Audio Spectrum Transformer 對音檔進行分類，並生成了前 10 個預測標籤及其相應的概率。在數據清理的初期階段，我們集中於識別和排除不相關的標籤。我們發現「Music」是最常見的標籤，其餘標籤大致可分為音樂樂器、噪聲或信號雜訊、高分貝聲音的描述、動物聲音、人類的談話或歌聲等類別。

在數據清理的初期階段，我們發現所有預測概率大於 0.7 且首要預測標籤不是 'Music' 的資料似乎都是不重要的，因此直接將其排除。隨後，我們假設那些標籤概率總和不足 0.7 的資料代表了預測成果較差。在這些資料中，我們排除了那些首要預測標籤為 'Music' 且與次要預測標籤概率差距在 0.1 之內的資料，因為這樣的預測結果表示最前面的兩組機率皆不高，完全可以剔除。

接下來，我們針對所有首要預測標籤為 'Music' 的資料進行了更深入的分析，並定義了一個特定的排除集合，用於篩選出那些不符合我們研究標準的標籤。如果這些數據中的其他任一標籤屬於這個集合且概率大於或等於 0.2，則將其排除。然後，我們減少了排除集合中的標籤數量，但將概率閾值提高到 0.5，以排除所有首要預測標籤非 'Music’、其他標籤屬於特定排除集合且任一標籤概率大於或等於 0.5 的資料。隨著這些步驟的進行，我們不斷更新排除集合，進行更細致的標籤分析，並逐步降低排除的概率閾值。這一系列步驟最終將 'Music' 標籤與其他標籤的界限明確劃分，直到排除閾值降至 0.2。

經過這些排除步驟後，我們轉向專注於吉他相關數據的細緻處理，確保這些數據中吉他的標籤概率高於其他樂器，從而更準確地反映吉他音頻的特性。此外，我們定義了一個包含集合，要求數據至少包含這些特定標籤，並排除不符合條件的資料。我們還針對特定類型的標籤進行了排除，例如鼓、靜音、語音等。最初階段的標籤總數為 457 個，這使得找出不需要的集合與需要的集合變得較為困難。由於標籤眾多，集體處理也變得更加複雜。而通過上述步驟，我們才能夠逐步地在最終階段將標籤數減少至約 100 個。

最後，我們對輸入和輸出數據進行了配對。無法成功配對的數據被剔除，確保了數據集的完整性和成對的一致性，為後續的訓練和分析提供了可靠的基礎。

To conduct research on guitar distortion removal (de-effect), we acquired a comprehensive dataset from the renowned guitar and bass multi-effect software manufacturer, Positive Grid LLC. This dataset includes a random assortment of audio files stored in the cloud by customers, encompassing both processed files using Positive Grid's amplifier and effect plugins, and unprocessed original recordings. Aligning with PG's original collection protocols, each audio file was precisely segmented into four-second clips, resulting in approximately 130,000 pairs of data, totaling 260,000 files. This information was meticulously organized and documented in CSV format.
Faced with varied audio quality and content within the dataset, we implemented a series of preprocessing steps to cleanse and filter the data. Initially, we utilized the "Audio Spectrum Transformer" to categorize our data, generating the top 10 predicted labels along with their corresponding probabilities. In the early stages of data cleansing, our focus was on identifying and excluding irrelevant labels. We noted that 'Music' was the most frequently occurring label, with the rest of the labels being broadly categorized into musical instruments, noise or signal interference, descriptions of loud sounds, animal sounds, and human speech or singing.

In the initial phase of data cleansing, we observed that all datasets with predictive probabilities above 0.7, where the top predicted label was not 'Music', seemed irrelevant and were therefore directly excluded. This was followed by the assumption that datasets with cumulative label probabilities under 0.7 indicated suboptimal predictive outcomes. Among these, we excluded those datasets where 'Music' was the top predicted label but had a probability gap of less than 0.1 with the secondary predicted label, as this indicated low confidence levels in the top two predictions and warranted their removal.
Subsequently, we conducted a deeper analysis on all datasets where 'Music' was the top predicted label, and we established a specific exclusion set to filter out labels that did not align with our research criteria. We excluded any other labels within these datasets that were part of the exclusion set and had a probability of 0.2 or higher. Following this, we reduced the number of labels in the exclusion set but increased the probability threshold to 0.5, thereby excluding all datasets where the primary predicted label was not 'Music', and other labels that were part of the exclusion set had a probability of 0.5 or higher.
Through these procedures, we continually refined the exclusion set, carrying out more detailed label analyses, and progressively lowered the probability threshold for exclusion. This process effectively segregated the 'Music' label from the others, ultimately reducing the exclusion threshold to 0.2.
After these steps, we shifted our focus to the meticulous processing of guitar-related data, ensuring that datasets prominently featured guitar labels over other instruments to more accurately reflect the characteristics of guitar audio. Furthermore, we formulated an inclusion set, mandating that datasets must contain these specific labels and excluded those that did not meet these criteria. We also excluded specific label categories, such as drums, silence, and speech.
Initially dealing with a total of 457 labels, distinguishing between the necessary and unnecessary sets proved challenging due to the sheer number of labels. The collective processing of such a large array of labels was complex. However, through the aforementioned steps, we successfully managed to reduce the number of labels to approximately 100 in the final phase.
Ultimately, we paired the input and output data. Datasets that could not be successfully paired were discarded, ensuring the integrity and consistency of the dataset, thus providing a reliable foundation for subsequent training and analysis.
