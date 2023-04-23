
import pptxgen from "pptxgenjs"

export function createPPTX() {
  let pptx = new pptxgen()
  genSlides_Master(pptx)
  pptx.writeFile({ fileName: 'Browser-PowerPoint-Demo.pptx' })
}

export function genSlides_Master(pptx) {
	pptx.addSection({ title: "Masters" })

	genSlide01(pptx)
	// genSlide02(pptx)
	// genSlide03(pptx)
	// genSlide04(pptx)
	// genSlide05(pptx)
	// genSlide06(pptx)
	//genSlide07(pptx)
}

/**
 * SLIDE 1:
 * @param {PptxGenJS} pptx
 */
function genSlide01(pptx) {
	let slide = pptx.addSlide({ masterName: "TITLE_SLIDE", sectionTitle: "Masters" })
	//let slide1 = pptx.addSlide({masterName:'TITLE_SLIDE', sectionTitle:'FAILTEST'}) // TEST: Should show console warning ("title not found")
	slide.addNotes("Master name: `TITLE_SLIDE`\nAPI Docs: https://gitbrent.github.io/PptxGenJS/docs/masters.html")
}

/**
 * SLIDE 2:
 * @param {PptxGenJS} pptx
 */
function genSlide02(pptx) {
	let slide = pptx.addSlide({ masterName: "MASTER_SLIDE", sectionTitle: "Masters" })
	slide.addNotes("Master name: `MASTER_SLIDE`\nAPI Docs: https://gitbrent.github.io/PptxGenJS/docs/masters.html")
}