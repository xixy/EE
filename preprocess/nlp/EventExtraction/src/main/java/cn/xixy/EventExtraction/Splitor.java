/**
 * @author xixy10@foxmail.com
 * @version V0.1 2018年8月30日 上午10:19:32
 */
package cn.xixy.EventExtraction;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import edu.stanford.nlp.pipeline.CoreDocument;
import edu.stanford.nlp.pipeline.CoreSentence;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;

/**
 *
 */
public class Splitor {

	public static List<String> split(String text) {
		List<String> SplittedSentences = new ArrayList<String>();
		Properties properties = new Properties();
		properties.setProperty("annotators", "tokenize, ssplit");
		// build pipeline
		StanfordCoreNLP pipeline = new StanfordCoreNLP(properties);
		// create a document object
		CoreDocument document = new CoreDocument(text);
		// annnotate the document
		pipeline.annotate(document);
		// I just gave a String constant which contains sentences.
		for (CoreSentence sentence : document.sentences()) {
			SplittedSentences.add(sentence.text());
			System.out.println(sentence.text());
		}
		return SplittedSentences;
	}

//	public static List<String> split(String text) {
//		List<String> SplittedSentences = new ArrayList<String>();
//		StanfordCoreNLP pipeline = new StanfordCoreNLP("StanfordCoreNLP-chinese.properties");
//		// pipeline.
//		// 创建一个解析器，传入的是需要解析的文本
//		Annotation annotation = new Annotation(text);
//
//		pipeline.annotate(annotation);
//		List<CoreMap> sentences = annotation.get(CoreAnnotations.SentencesAnnotation.class);
//		System.out.println(sentences.size());
//		for (CoreMap sentence : sentences) {
//			SplittedSentences.add(sentence.toString());
//		}
//		return SplittedSentences;
//	}

	/**
	 * 处理文件句子，每一句都是一段
	 * 
	 * @param filepath
	 *            文件路径
	 */
	public static void splitFileSentence(String filepath, String targetFilePath) {
		File source_file = new File(filepath);
		File writename = new File(targetFilePath);
		BufferedWriter out = null;
		try {
			writename.createNewFile();
			out = new BufferedWriter(new FileWriter(writename));
		} catch (IOException e1) {
			e1.printStackTrace();
		} // 创建新文件


		if (source_file.exists()) {
			try {
				FileReader fileReader = new FileReader(source_file);
				BufferedReader br = new BufferedReader(fileReader);
				String lineContent = null;
				while ((lineContent = br.readLine()) != null) {
					/*
					 * 如果是文件名称/
					 */
					if(lineContent.startsWith("../../data")){
						System.out.println(lineContent);
						out.write(lineContent + "\r\n");
					}
					/*
					 * 如果是文本内容
					 */
					else{
						for(String sentence:split(lineContent)){
							// 去掉空格
							sentence = sentence.replace(" ", "");
							// 去掉
							out.write(sentence + "\r\n");
						}

					}
				}
				br.close();
				fileReader.close();
				out.flush(); // 把缓存区内容压入文件
				out.close(); // 最后记得关闭文件
			} catch (FileNotFoundException e) {
				System.out.println("no this file");
				e.printStackTrace();
			} catch (IOException e) {
				System.out.println("io exception");
				e.printStackTrace();
			}
		}


	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {

		String targetFilePath = "/Users/apple/Documents/开题报告/开题报告/代码/event_extraction/EventExtractionProject/preprocess/extractor/sentences.txt";
		String file_path = "/Users/apple/Documents/开题报告/开题报告/代码/event_extraction/EventExtractionProject/preprocess/extractor/param_as_sentence.dat";
		String text = "通过这次对习近平总书记“十九大”报告的学习，我对我们国家的发展、我们国家所处的历史时期以及我们国家的国际地位都有了新的认识。我也更加清晰的看到了我们党对我们国家发展路线的明确规划。作为党员，自己也更加清晰自己的努力方向。我们一定要“不忘初心，牢记使命”，做一名为党和国家创造价值和利益的合格的共产党员。";
		String text2 = "京津冀以外，蔡国雄还看好中国西部的一些地区\"西部大开发已经谈了五年了，成功了吗？坦白说发展还不够快，中国政府也意识到了这一点。\"";
		splitFileSentence(file_path, targetFilePath);
//		 System.out.println(Splitor.split(text2));

	}

}
