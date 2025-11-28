import Foundation
import PDFKit

struct PDFExtractor {
    static func run() {
        guard CommandLine.arguments.count > 1 else {
            fputs("Usage: pdf_to_text <file> [<file> ...]\n", stderr)
            exit(1)
        }

        for path in CommandLine.arguments.dropFirst() {
            let url = URL(fileURLWithPath: path)
            guard let document = PDFDocument(url: url) else {
                fputs("Failed to open \(path)\n", stderr)
                continue
            }
            var buffer = ""
            for index in 0..<document.pageCount {
                if let page = document.page(at: index) {
                    buffer.append(page.string ?? "")
                    buffer.append("\n")
                }
            }
            print("===== \(path) =====")
            print(buffer)
        }
    }
}

PDFExtractor.run()
