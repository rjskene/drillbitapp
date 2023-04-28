import titleImage from '../assets/pptx/title_image.png'
import masterHeader from '../assets/pptx/slide_header.png'
import masterFooter from '../assets/pptx/slide_footer.png'
import pptxgen from 'pptxgenjs'

import { useFormatHelpers, every_nth } from './composables'
import {
  useStatementStore,
} from '@/stores/modules'


const format = useFormatHelpers()
const statStore = useStatementStore()
const labelFormatCodes = {
	block_schedule: format.btcStr + '#,##0',
	bitcoin_price: '$#,##0',
	transaction_fees: format.btcStr + '#0.00',
	hash_rate: '#,##0" EH/s"',
}
const colors = {
	blue: '2F5597',
	darkBlue: '273962',
	green: '80ba56',
}
const lineColorSequence = [colors.blue, colors.green]
const headerOpts = { 
	bold: true, fill: colors.darkBlue, 
	color: 'ffffff', valign: 'middle', align: 'center'
}

export async function createPPTX(elements, group, summary) {
  let pres = new ProjectComparisonPresentation()
	pres.createMasters()
	pres.createTitleSlide()
	pres.createSummarySlide()
	pres.createProjectsSlide(group)
	pres.createEnviroSlide(elements)
	pres.createResultsSlides(summary)
  pres.pptx.writeFile({ fileName: 'Sample Pres.pptx' })
}

class ProjectComparisonPresentation {
	constructor() {
		this.pptx = new pptxgen()
	}
	createMasters() {	
		const headerImage = { 
			x: '0%', y: '3%', w: '95%', h: '13.25%', 
			path: masterHeader,
		}
		const footerImage ={ 
			x: '0%', y: '87%', w: '95%', h: '13.25%', 
			path: masterFooter,
		}
		const titlePlaceholder = {
			text: 'Add title',
			options: { 
				name: 'title', type: 'title', 
				x: '3%', y: '0%', w: '90%', h: '10%',
				color: colors.blue, fontSize: 24, fontFace: 'Calibri (Body)', 
				bold: true, align: 'left',
			}
		}
		const bodyPlaceholder = {
			text: 'Add text',
			options: { 
				name: 'body', type: 'body', 
				x: '3%', y: '15%', w: '90%', h: '70%',
				color: colors.blue, fontSize: 18, fontFace: 'Calibri (Body)', 
				bold: true, align: 'left', bullet: true
			}
		}
		this.pptx.defineSlideMaster({
			title: 'TITLE_SLIDE',
			background: { color: 'FFFFFF' },
			objects: [
				{
					image: { 
						x: '0%', y: '50%', w: '100%', h: '50%', 
						path: titleImage,
					},
				}, {
					placeholder: {
						options: { 
							name: 'title', type: 'title', 
							x: '20%', y: '37%', w: '70.5%', h: '5%',
							color: '2F5597', fontSize: 32, fontFace: 'Calibri (Body)', 
							bold: true, align: 'right',
						},
						text: 'Add title',
					 }, 
				},
			],
		})
		this.pptx.defineSlideMaster({
			title: 'MASTER_SLIDE_W_BODY',
			background: { color: 'FFFFFF' },
			objects: [
				{
					placeholder: {
						text: 'Add title',
						options: { 
							name: 'title', type: 'title', 
							x: '3%', y: '0%', w: '90%', h: '10%',
							color: colors.blue, fontSize: 24, fontFace: 'Calibri (Body)', 
							bold: true, align: 'left',
						}
					},
				}, {
					image: headerImage,
				}, {
					placeholder: bodyPlaceholder,
				}, {
					image: footerImage,
				}
			]
		})
		this.pptx.defineSlideMaster({
			title: 'MASTER_SLIDE_NO_BODY',
			background: { color: 'FFFFFF' },
			objects: [
				{
					placeholder: titlePlaceholder,
				}, {
					image: headerImage,
				}, {
					image: footerImage,
				}
			]
		})			
	}
	createTitleSlide() {
		this.pptx.addSection({ title: 'Title' })
		let slide = this.pptx.addSlide({ masterName: 'TITLE_SLIDE' })
		slide.addText('Project Analysis 2023-04-26', { placeholder: 'title' })
	}
	createSummarySlide() {
		this.pptx.addSection({ title: 'Summary' })
		const slide = this.pptx.addSlide({ masterName: 'MASTER_SLIDE_W_BODY', sectionTitle: 'Summary' })
		slide.addText('Summary', { placeholder: 'title' })
	}
	createProjectsSlide(group) {
		this.pptx.addSection({title: 'Projects'})
		const slide = this.pptx.addSlide({ masterName: 'MASTER_SLIDE_NO_BODY', sectionTitle: 'Projects' })
		slide.addText('Projects - ' + group.name, { placeholder: 'title'})

		const arrRows = []
		arrRows.push([
			{ text: 'Name', options: {...headerOpts, align: 'left'} },
			{ text: 'Capacity', options: headerOpts },
			{ text: 'OC', options: headerOpts },
			{ text: 'Energy Price', options: headerOpts },
			// { text: 'Opex', options: headerOpts },
			{ text: 'Pool Fees', options: headerOpts },
			{ text: 'Property Tax', options: headerOpts },
			{ text: 'Income Tax', options: headerOpts },
			{ text: 'Cost', options: headerOpts },
		])
		group.projects.forEach((project, idx) => {
			arrRows.push([
				{ text: project.name, options: { valign: 'middle' } },
				{ text: format.power(project.capacity), options: { valign: 'middle', align: 'center' } },
				{ text: project.target_overclocking + 'x', options: { valign: 'middle', align: 'center' } },
				{ text: format.energyPrice(project.energy_price), options: { valign: 'middle', align: 'center' } },
				// { text: project.opex, options: { valign: 'middle', align: 'center' } },
				{ text: format.percentage(project.pool_fees), options: { valign: 'middle', align: 'center' } },
				{ text: format.percentage(project.property_taxes), options: { valign: 'middle', align: 'center' } },
				{ text: format.percentage(project.tax_rate), options: { valign: 'middle', align: 'center' } },
				{ text: format.currency(project.total_capital_cost), options: { valign: 'middle', align: 'center' } },
			])
		})
		slide.addTable(
			arrRows, { 
				x: '3%', y: '15%',
				colW: [1.75, .9, .65, .9, .9, .9, .9, 1.25], 
				margin: 0.05, 
				border: { color: 'CFCFCF' }, autoPage: true 
			}
		)

		for (let project of group.projects) {
			const slide = this.pptx.addSlide({ masterName: 'MASTER_SLIDE_NO_BODY', sectionTitle: 'Projects' })
			slide.addText('Project - ' + project.name, { placeholder: 'title'})

			slide.addText('Rigs', { 
				x: '3%', y: '15%', fontSize: 18, bold: true, color: colors.blue 
			})
			const rigRows = []
			rigRows.push([
				{ text: 'Name', options: {...headerOpts, align: 'left'} },
				{ text: 'Power', options: headerOpts },
				{ text: 'Hash Rate', options: headerOpts },
				{ text: 'Efficiency', options: headerOpts },
				{ text: 'Price', options: headerOpts },
				{ text: 'Quantity', options: headerOpts },
				{ text: 'Cost', options: headerOpts },
			])
			project.rigs.forEach((rig, idx) => {
				rigRows.push([
					{ text: rig.rig.name, options: { valign: 'middle' } },
					{ text: format.power(rig.rig.power), options: { valign: 'middle', align: 'center' } },
					{ text: format.hashRate(rig.rig.hash_rate), options: { valign: 'middle', align: 'center' } },
					{ text: format.efficiency(rig.rig.efficiency), options: { valign: 'middle', align: 'center' } },
					{ text: format.currency(rig.price), options: { valign: 'middle', align: 'center' } },
					{ text: Math.round(rig.quantity), options: { valign: 'middle', align: 'center' } },
					{ text: format.currency(rig.cost), options: { valign: 'middle', align: 'center' } },
				])
			})
			slide.addTable(
				rigRows, { 
					x: '3%', y: '20%',
					colW: [1.75, .9, .9, .9, .9, .9, 1.25], 
					margin: 0.05, 
					border: { color: 'CFCFCF' }, autoPage: true 
				}
			)

			slide.addText('Infrastructure', { 
				x: '3%', y: '40%', fontSize: 18, bold: true, color: colors.blue 
			})

			const infraRows = []
			infraRows.push([
				{ text: 'Type', options: {...headerOpts, align: 'left'} },
				{ text: 'Name', options: {...headerOpts, align: 'left'} },
				{ text: 'Capacity', options: headerOpts },
				{ text: 'PUE', options: headerOpts },
				{ text: 'Price', options: headerOpts },
				{ text: 'Quantity', options: headerOpts },
				{ text: 'Cost', options: headerOpts },
			])
			project.infrastructure.forEach((infra, idx) => {
				infraRows.push([
					{ text: infra.infra_content_type, options: { valign: 'middle' } },
					{ text: infra.infrastructure.name, options: { valign: 'middle' } },
					{ text: format.power(infra.infrastructure.capacity), options: { valign: 'middle', align: 'center' } },
					{ text: infra.infrastructure.pue + 'x', options: { valign: 'middle', align: 'center' } },
					{ text: format.currency(infra.price), options: { valign: 'middle', align: 'center' } },
					{ text: Math.round(infra.quantity), options: { valign: 'middle', align: 'center' } },
					{ text: format.currency(infra.cost), options: { valign: 'middle', align: 'center' } },
				])
			})
			slide.addTable(
				infraRows, { 
					x: '3%', y: '45%',
					colW: [1.5, 2.5, .9, .9, .9, .9, 1.25], 
					margin: 0.05, 
					border: { color: 'CFCFCF' }, autoPage: true 
				}
			)
		}		
	}
	createEnviroSlide(elements) {
		this.pptx.addSection({ title: 'Environment' })
		const slide = this.pptx.addSlide({ masterName: 'MASTER_SLIDE_NO_BODY', sectionTitle: 'Environment' })
		slide.addText('Environment', { placeholder: 'title' })
		
		elements.forEach((element, idx) => {
			const chartData = []
			let data = element.store.object?.data
			data = every_nth(data, 1000)

			// makes labels
			let labels = []
			data.forEach((object) => {
				let date = new Date(object['period'] + ':00')
				let year = date.toLocaleString('default', { year: 'numeric' })
				let month = date.toLocaleString('default', { month: 'short' })
				labels.push(month + '\n' + year)
			})
			labels[0] = '' // don't show first label

			// makes values
			let values = data.map((object) => object[element.dataKey])
			chartData.push({
				name: element.text,
				labels,
				values
			})

			const nMajorAxisLabels = 5	
			const catAxisLabelFrequency = Math.round(labels.length / nMajorAxisLabels)
			const intWgap = 4.75
			const xSpacers = [0.125, .05, 0, 0]
			const wSpacers = [-.25, 0, 0, 0]

			slide.addChart(this.pptx.charts.LINE, chartData, {
				x: (idx < 2 ? idx * intWgap : (idx - 2) * intWgap ) + xSpacers[idx],
				y: idx < 2 ? 0.5 : 2.65,
				w: 4.75 + wSpacers[idx],
				h: idx < 2 ? 2.30 : 2.65,
				chartColors: lineColorSequence,
				lineDataSymbol: 'none',
				showTitle: true,
				title: element.text,
				titleFontSize: 14,
				titleColor: colors.blue,
				catAxisHidden: idx < 2,
				catAxisLineShow: true,
				catAxisLabelFrequency,
				catAxisLabelFontSize: 12,
				catAxisMajorTickMark: 'none',
				catGridLine: {color: 'FFFFFF'},
				valGridLine: {color: 'FFFFFF'},
				valAxisLabelFormatCode: labelFormatCodes[element.key]
			})
		})
	}
	createResultsSlides(summary) {
		this.pptx.addSection({ title: 'Results' })
		
		var slide = this.pptx.addSlide({ masterName: 'MASTER_SLIDE_NO_BODY', sectionTitle: 'Results' })
		slide.addText('Results - Metrics', { placeholder: 'title' })

		var summaryRows = statStore.summaryGroups[0]
		var data = summary.filter((obj) => summaryRows.includes(obj.index))

		var rows = []
		rows.push([{ text: '', options: {...headerOpts, align: 'left'} }])
		Object.keys(data[0]).slice(1).forEach((key) => {
			rows[0].push({ text: key, options: {...headerOpts, align: 'center'} })
		})

		var valueFormats = {
			'Capacity': format.power,
			'Compute Power': format.power,
			'Infra Power': format.power,
			'Number of Rigs': format.number,
			'Hash Rate': format.hashRate,
			'Total Hashes': format.hashRate,
			'Energy Consumption': format.power,
			'Efficiency': format.efficiency,
			'BTC, held': format.BTC,
			'Breakeven': val => val
		}
		Object.entries(statStore.summaryFormatByRow)
			.forEach(([key, value]) => {
				value.forEach((row) => {
					valueFormats[row] = format[key]
				})
			})
		data.forEach((row, idx) => {
			Object.values(row).forEach((value, idx2) => {
				if (idx2 === 0) {
					rows.push([{ text: value, options: {align: 'left'} }])
				} else {
					rows[idx + 1].push({ text: valueFormats[row.index](value), options: {align: 'center'} })
				}
			})
		})
		slide.addTable(
			rows, { 
				x: '3%', y: '15%',
				// colW: [1.5, 2.5, .9, .9, .9, .9, 1.25], 
				margin: 0.05, 
				border: { color: 'CFCFCF' }, autoPage: true 
			}
		)

		slide = this.pptx.addSlide({ masterName: 'MASTER_SLIDE_NO_BODY', sectionTitle: 'Results' })
		slide.addText('Results - Costs', { placeholder: 'title' })

		var summaryRows = statStore.summaryGroups[1]
		var data = summary.filter((obj) => summaryRows.includes(obj.index))

		rows = []
		rows.push([{ text: '', options: {...headerOpts, align: 'left'} }])
		Object.keys(data[0]).slice(1).forEach((key) => {
			rows[0].push({ text: key, options: {...headerOpts, align: 'center'} })
		})
		data.forEach((row, idx) => {
			Object.values(row).forEach((value, idx2) => {
				if (idx2 === 0) {
					rows.push([{ text: value, options: {align: 'left'} }])
				} else {
					rows[idx + 1].push({ text: valueFormats[row.index](value), options: {align: 'center'} })
				}
			})
		})
		slide.addTable(
			rows, { 
				x: '3%', y: '15%',
				// colW: [1.5, 2.5, .9, .9, .9, .9, 1.25], 
				margin: 0.05, 
				border: { color: 'CFCFCF' }, autoPage: true 
			}
		)

		slide = this.pptx.addSlide({ masterName: 'MASTER_SLIDE_NO_BODY', sectionTitle: 'Results' })
		slide.addText('Results - Profitability', { placeholder: 'title' })

		var summaryRows = statStore.summaryGroups[2]
		var data = summary.filter((obj) => summaryRows.includes(obj.index))

		rows = []
		rows.push([{ text: '', options: {...headerOpts, align: 'left'} }])
		Object.keys(data[0]).slice(1).forEach((key) => {
			rows[0].push({ text: key, options: {...headerOpts, align: 'center'} })
		})
		data.forEach((row, idx) => {
			Object.values(row).forEach((value, idx2) => {
				if (idx2 === 0) {
					rows.push([{ text: value, options: {align: 'left'} }])
				} else {
					rows[idx + 1].push({ text: valueFormats[row.index](value), options: {align: 'center'} })
				}
			})
		})
		slide.addTable(
			rows, { 
				x: '3%', y: '15%',
				// colW: [1.5, 2.5, .9, .9, .9, .9, 1.25], 
				margin: 0.05, 
				border: { color: 'CFCFCF' }, autoPage: true 
			}
		)
	}
}